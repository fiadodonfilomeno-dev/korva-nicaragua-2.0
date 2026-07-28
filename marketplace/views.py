from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Sum, Count
from .models import Product, ProductFavorite, Review, Deal, Transaction, BankAccount, PayoutRequest
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


@login_required(login_url='login')
def export_catalog_pdf(request):
    """Exportar catalogo de productos del usuario actual como PDF"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet
    from io import BytesIO
    from datetime import datetime
    import os

    profile = request.user.profile
    products = profile.products.filter(is_active=True)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []

    # Header
    title_style = styles['Title']
    story.append(Paragraph(f"Catalogo de Productos", title_style))
    story.append(Paragraph(f"{profile.business_name} - {profile.get_city_display()}", styles['Heading2']))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 1*cm))

    if not products.exists():
        story.append(Paragraph("No hay productos en el catalogo.", styles['Normal']))
    else:
        # Productos
        for i, p in enumerate(products, 1):
            story.append(Paragraph(f"{i}. {p.name}", styles['Heading3']))
            story.append(Paragraph(f"Categoria: {p.get_category_display()}", styles['Normal']))
            story.append(Paragraph(f"Precio: ${p.price}", styles['Normal']))
            if p.description:
                story.append(Paragraph(p.description[:200], styles['Normal']))
            if p.image and os.path.exists(p.image.path):
                try:
                    story.append(RLImage(p.image.path, width=5*cm, height=5*cm))
                except:
                    pass
            story.append(Paragraph(f"Vistas: {p.views_count} | Activo: {'Si' if p.is_active else 'No'}", styles['Normal']))
            story.append(Spacer(1, 0.5*cm))

            if i % 4 == 0:
                doc.build(story)
                story = []

    if story:
        doc.build(story)

    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="catalogo_{profile.business_name}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    return response


@login_required(login_url='login')
def buy_product(request, product_id):
    """Iniciar compra de un producto"""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    buyer = request.user.profile

    if buyer == product.user:
        messages.error(request, 'No puedes comprar tu propio producto.')
        return redirect('product_detail', product_id=product.pk)

    if request.method == 'POST':
        bank = request.POST.get('bank', '')
        notes = request.POST.get('notes', '')
        Transaction.objects.create(
            product=product, buyer=buyer, seller=product.user,
            amount=product.price, currency=product.currency, bank=bank,
            buyer_notes=notes,
        )
        messages.success(request, 'Solicitud de compra creada. Transfiere el monto al vendedor usando los datos bancarios.')
        return redirect('my_purchases')

    return render(request, 'marketplace/checkout.html', {'product': product})


@login_required(login_url='login')
def my_purchases(request):
    """Compras realizadas por el usuario"""
    transactions = Transaction.objects.filter(buyer=request.user.profile).select_related('product', 'seller')
    return render(request, 'marketplace/my_purchases.html', {'transactions': transactions})


@login_required(login_url='login')
def my_sales(request):
    """Ventas recibidas (productos del usuario)"""
    transactions = Transaction.objects.filter(seller=request.user.profile).select_related('product', 'buyer')
    return render(request, 'marketplace/my_sales.html', {'transactions': transactions})


@login_required(login_url='login')
def transaction_detail(request, transaction_id):
    """Detalle de una transaccion"""
    profile = request.user.profile
    txn = get_object_or_404(Transaction, pk=transaction_id)
    if txn.buyer != profile and txn.seller != profile:
        messages.error(request, 'No tienes acceso a esta transaccion.')
        return redirect('marketplace')
    bank_acct = BankAccount.objects.filter(seller=txn.seller).first()
    return render(request, 'marketplace/transaction_detail.html', {'txn': txn, 'bank_acct': bank_acct})


@login_required(login_url='login')
@require_POST
def confirm_payment(request, transaction_id):
    """Comprador marca el pago como realizado"""
    txn = get_object_or_404(Transaction, pk=transaction_id, buyer=request.user.profile)
    if txn.status == 'pending':
        txn.status = 'paid'
        from django.utils import timezone
        txn.payment_date = timezone.now()
        txn.save()
        messages.success(request, 'Pago reportado. El vendedor confirmara la recepcion.')
    return redirect('transaction_detail', transaction_id=txn.pk)


@login_required(login_url='login')
@require_POST
def confirm_receipt(request, transaction_id):
    """Vendedor confirma que recibio el pago"""
    txn = get_object_or_404(Transaction, pk=transaction_id, seller=request.user.profile)
    if txn.status == 'paid':
        txn.status = 'confirmed'
        txn.save()
        messages.success(request, 'Pago confirmado. Los fondos estan en tu cuenta.')
    return redirect('transaction_detail', transaction_id=txn.pk)


@login_required(login_url='login')
@require_POST
def complete_transaction(request, transaction_id):
    """Completar transaccion (vendedor)"""
    txn = get_object_or_404(Transaction, pk=transaction_id, seller=request.user.profile)
    if txn.status == 'confirmed':
        txn.status = 'completed'
        txn.save()
        messages.success(request, 'Transaccion completada exitosamente.')
    return redirect('transaction_detail', transaction_id=txn.pk)


@login_required(login_url='login')
@require_POST
def cancel_transaction(request, transaction_id):
    """Cancelar transaccion (cualquier parte)"""
    txn = get_object_or_404(Transaction, pk=transaction_id)
    if request.user.profile not in (txn.buyer, txn.seller):
        messages.error(request, 'No tienes permiso.')
        return redirect('marketplace')
    if txn.status in ('pending', 'paid'):
        txn.status = 'cancelled'
        txn.save()
        messages.success(request, 'Transaccion cancelada.')
    return redirect('transaction_detail', transaction_id=txn.pk)


@login_required(login_url='login')
def seller_wallet(request):
    """Wallet del vendedor - balance y payouts"""
    profile = request.user.profile
    sales = Transaction.objects.filter(seller=profile)
    total_earned = sales.filter(status='completed').aggregate(s=Sum('seller_amount'))['s'] or 0
    total_commission = sales.filter(status='completed').aggregate(s=Sum('commission_amount'))['s'] or 0
    pending_sales = sales.filter(status__in=('paid', 'confirmed')).aggregate(s=Sum('amount'))['s'] or 0
    payouts = PayoutRequest.objects.filter(seller=profile)
    payouts_total = payouts.filter(status='completed').aggregate(s=Sum('amount'))['s'] or 0
    available_balance = total_earned - payouts_total
    bank_acct = BankAccount.objects.filter(seller=profile).first()

    context = {
        'total_earned': total_earned,
        'total_commission': total_commission,
        'pending_sales': pending_sales,
        'available_balance': available_balance,
        'payouts': payouts,
        'bank_acct': bank_acct,
        'sales_count': sales.filter(status='completed').count(),
    }
    return render(request, 'marketplace/seller_wallet.html', context)


@login_required(login_url='login')
def bank_account_view(request):
    """Administrar cuenta bancaria del vendedor"""
    profile = request.user.profile
    acct = BankAccount.objects.filter(seller=profile).first()

    if request.method == 'POST':
        bank = request.POST.get('bank')
        account_type = request.POST.get('account_type', 'monetaria')
        account_number = request.POST.get('account_number', '')
        account_holder = request.POST.get('account_holder', '')
        id_number = request.POST.get('id_number', '')
        phone = request.POST.get('phone', '')

        if acct:
            acct.bank = bank
            acct.account_type = account_type
            acct.account_number = account_number
            acct.account_holder = account_holder
            acct.id_number = id_number
            acct.phone = phone
            acct.verified = False
            acct.save()
        else:
            BankAccount.objects.create(
                seller=profile, bank=bank, account_type=account_type,
                account_number=account_number, account_holder=account_holder,
                id_number=id_number, phone=phone,
            )
        messages.success(request, 'Cuenta bancaria guardada. Nuestro equipo verificara los datos.')
        return redirect('seller_wallet')

    return render(request, 'marketplace/bank_account.html', {'acct': acct})


@login_required(login_url='login')
@require_POST
def request_payout(request):
    """Solicitar retiro de fondos"""
    profile = request.user.profile
    amount = request.POST.get('amount', 0)
    acct = BankAccount.objects.filter(seller=profile, verified=True).first()

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        messages.error(request, 'Monto invalido.')
        return redirect('seller_wallet')

    if amount <= 0:
        messages.error(request, 'El monto debe ser mayor a cero.')
        return redirect('seller_wallet')

    if not acct:
        messages.error(request, 'Necesitas registrar una cuenta bancaria verificada.')
        return redirect('bank_account')

    PayoutRequest.objects.create(seller=profile, amount=amount, bank_account=acct)
    messages.success(request, 'Solicitud de retiro enviada. Procesaremos en 1-3 dias habiles.')
    return redirect('seller_wallet')

