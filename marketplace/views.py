from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Product, ProductFavorite, Review, Deal
from .forms import ProductForm

def marketplace(request):
    """Vista principal del marketplace"""
    products = Product.objects.select_related('user').filter(is_active=True)
    
    # Filtrar por categoría
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    
    # Buscar productos
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(user__business_name__icontains=search_query)
        )
    
    # Ordenar (whitelist para evitar inyección)
    allowed_sorts = {'created_at', '-created_at', 'price', '-price', 'views_count', '-views_count', 'name', '-name'}
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by not in allowed_sorts:
        sort_by = '-created_at'
    products = products.order_by(sort_by)
    
    context = {
        'products': products,
        'category': category,
        'search_query': search_query,
    }
    
    return render(request, 'marketplace/marketplace.html', context)


@login_required(login_url='login')
def create_product(request):
    """Vista para crear un nuevo producto"""
    try:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.user = request.user.profile
                product.save()
                messages.success(request, 'Producto publicado exitosamente.')
                return redirect('marketplace')
        else:
            form = ProductForm()
        
        return render(request, 'marketplace/create_product.html', {'form': form})
    except Exception as e:
        messages.error(request, f'Error al crear producto: {str(e)}')
        return redirect('marketplace')


def product_detail(request, product_id):
    """Vista de detalle de un producto"""
    product = get_object_or_404(Product, pk=product_id)
    product.views_count += 1
    product.save()
    
    # Productos similares
    similar_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=product.pk)[:5]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    
    return render(request, 'marketplace/product_detail.html', context)


@login_required(login_url='login')
def edit_product(request, product_id):
    """Editar un producto"""
    try:
        product = get_object_or_404(Product, pk=product_id)
        
        if product.user != request.user.profile:
            messages.error(request, 'No tienes permiso para editar este producto.')
            return redirect('product_detail', product_id=product.pk)
        
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto actualizado.')
                return redirect('product_detail', product_id=product.pk)
        else:
            form = ProductForm(instance=product)
        
        return render(request, 'marketplace/edit_product.html', {'form': form, 'product': product})
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('marketplace')


@login_required(login_url='login')
def delete_product(request, product_id):
    """Eliminar un producto"""
    try:
        product = get_object_or_404(Product, pk=product_id)
        
        if product.user != request.user.profile:
            messages.error(request, 'No tienes permiso para eliminar este producto.')
            return redirect('product_detail', product_id=product.pk)
        
        if request.method == 'POST':
            product.delete()
            messages.success(request, 'Producto eliminado.')
            return redirect('marketplace')
        
        return render(request, 'marketplace/confirm_delete.html', {'product': product})
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('marketplace')


@login_required(login_url='login')
def my_products(request):
    """Ver los productos del usuario actual"""
    try:
        products = request.user.profile.products.all()
        
        context = {
            'products': products,
        }
        
        return render(request, 'marketplace/my_products.html', context)
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('marketplace')


@login_required(login_url='login')
@require_POST
def toggle_favorite_product(request, product_id):
    """Agregar/quitar producto de favoritos"""
    product = get_object_or_404(Product, pk=product_id)
    user_profile = request.user.profile
    fav, created = ProductFavorite.objects.get_or_create(user=user_profile, product=product)
    if not created:
        fav.delete()
        is_fav = False
    else:
        is_fav = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_fav, 'count': product.favorited_by.count()})
    return redirect('product_detail', product_id=product.pk)


@login_required(login_url='login')
def my_favorites(request):
    """Ver favoritos del usuario"""
    from social.models import Post
    user_profile = request.user.profile
    fav_posts = Post.objects.filter(favorited_by__user=user_profile)
    fav_products = Product.objects.filter(favorited_by__user=user_profile)
    context = {'fav_posts': fav_posts, 'fav_products': fav_products}
    return render(request, 'marketplace/my_favorites.html', context)


@login_required(login_url='login')
@require_POST
def add_review(request, username):
    """Agregar calificacion a un vendedor"""
    from users.models import Profile as UserProfile
    seller = get_object_or_404(UserProfile, user__username=username)
    reviewer = request.user.profile
    if seller == reviewer:
        messages.error(request, 'No puedes calificarte a ti mismo.')
        return redirect('profile', username=username)
    rating = request.POST.get('rating', 5)
    comment = request.POST.get('comment', '')
    product_id = request.POST.get('product_id')
    product = None
    if product_id:
        product = Product.objects.filter(pk=product_id).first()
    Review.objects.update_or_create(
        reviewer=reviewer, seller=seller, product=product,
        defaults={'rating': int(rating), 'comment': comment}
    )
    messages.success(request, 'Calificacion enviada.')
    return redirect('profile', username=username)


def seller_reviews(request, username):
    """Ver calificaciones de un vendedor"""
    from users.models import Profile as UserProfile
    seller = get_object_or_404(UserProfile, user__username=username)
    reviews = Review.objects.filter(seller=seller).select_related('reviewer', 'product')
    avg = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
    context = {'seller': seller, 'reviews': reviews, 'avg_rating': round(avg, 1)}
    return render(request, 'marketplace/seller_reviews.html', context)


def deals_list(request):
    """Lista de ofertas activas"""
    from django.utils import timezone
    deals = Deal.objects.filter(is_active=True, ends_at__gt=timezone.now()).select_related('product', 'seller')
    context = {'deals': deals}
    return render(request, 'marketplace/deals_list.html', context)


@login_required(login_url='login')
def create_deal(request, product_id):
    """Crear oferta para un producto"""
    product = get_object_or_404(Product, pk=product_id)
    if product.user != request.user.profile:
        messages.error(request, 'No tienes permiso.')
        return redirect('marketplace')
    if request.method == 'POST':
        from django.utils import timezone as tz
        from datetime import datetime
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        discount = int(request.POST.get('discount_percent', 0))
        ends = request.POST.get('ends_at', '')
        if title and discount > 0:
            deal_price = float(product.price) * (1 - discount / 100)
            Deal.objects.create(
                product=product, seller=request.user.profile, title=title,
                description=description, discount_percent=discount,
                original_price=product.price, deal_price=deal_price,
                starts_at=tz.now(), ends_at=datetime.fromisoformat(ends)
            )
            messages.success(request, 'Oferta creada.')
            return redirect('product_detail', product_id=product.pk)
    return render(request, 'marketplace/create_deal.html', {'product': product})

