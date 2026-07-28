from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q
from django.utils import timezone
from .models import Post, Comment, PostImage, Vote, Favorite
from .forms import PostForm, CommentForm, PostImageForm
from users.models import Profile
from notifications.utils import create_notification

def home(request):
    """Vista principal - Landing si no autenticado, Muro Social si autenticado"""
    if not request.user.is_authenticated:
        return render(request, 'landing.html')
    
    try:
        posts = Post.objects.select_related('author').filter(moderation_status='approved')
        
        # Buscar posts
        search_query = request.GET.get('q')
        tag_query = request.GET.get('tag')
        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__business_name__icontains=search_query)
            )
        if tag_query:
            posts = posts.filter(tags__name__in=[tag_query])
        
        context = {
            'posts': posts,
            'search_query': search_query,
            'tag_query': tag_query,
        }
        
        return render(request, 'social/home.html', context)
    except Exception as e:
        messages.error(request, f'Error al cargar el muro: {str(e)}')
        return redirect('home')


@login_required(login_url='login')
@require_GET
def check_new_posts(request):
    """AJAX: verifica si hay posts nuevos desde una marca de tiempo"""
    last_id = request.GET.get('last_id', 0, type=int)
    new_count = Post.objects.filter(
        moderation_status='approved',
        id__gt=last_id
    ).count()
    return JsonResponse({'new_count': new_count})


@login_required(login_url='login')
def create_post(request):
    """Vista para crear un nuevo post"""
    try:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user.profile
                post.save()
                form.save_m2m()  # Guardar tags
                
                # Guardar imágenes adicionales (galería)
                gallery_images = request.FILES.getlist('gallery')
                for img in gallery_images:
                    PostImage.objects.create(post=post, image=img)
                
                messages.success(request, 'Post publicado exitosamente.')
                return redirect('home')
        else:
            form = PostForm()
        
        return render(request, 'social/create_post.html', {'form': form})
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('home')


def post_detail(request, post_id):
    """Vista de detalle de un post"""
    post = get_object_or_404(Post, pk=post_id, moderation_status='approved')
    comments = post.comments.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.profile
            comment.save()
            messages.success(request, 'Comentario publicado.')
            return redirect('post_detail', post_id=post.pk)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    
    return render(request, 'social/post_detail.html', context)


@login_required(login_url='login')
@require_POST
def upvote_post(request, post_id):
    """Aumentar votos positivos en un post (un voto por usuario)"""
    try:
        post = get_object_or_404(Post, pk=post_id)
        user_profile = request.user.profile
        
        # Verificar si ya votó
        existing_vote = Vote.objects.filter(user=user_profile, post=post).first()
        
        if existing_vote:
            if existing_vote.vote_type == 'up':
                # Ya votó up, quitar voto
                existing_vote.delete()
                post.upvotes = max(0, post.upvotes - 1)
                post.author.popularity_score = max(0, post.author.popularity_score - 10)
                vote_action = 'removed'
            else:
                # Cambió de down a up
                existing_vote.vote_type = 'up'
                existing_vote.save()
                post.upvotes += 1
                post.downvotes = max(0, post.downvotes - 1)
                post.author.popularity_score += 15  # +10 up +5 por quitar down
                vote_action = 'changed_to_up'
        else:
            # Nuevo voto up
            Vote.objects.create(user=user_profile, post=post, vote_type='up')
            post.upvotes += 1
            post.author.popularity_score += 10
            vote_action = 'upvoted'
            create_notification(
                recipient=post.author.user,
                sender=request.user,
                notification_type='like',
                title='Te dieron un like',
                message=f'A {request.user.profile.business_name or request.user.username} le gustó tu publicación',
                related_object_id=post.id,
                related_object_type='post',
            )
        
        post.author.save()
        post.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'upvotes': post.upvotes,
                'downvotes': post.downvotes,
                'author_score': post.author.popularity_score,
                'action': vote_action,
                'user_vote': 'up' if vote_action in ['upvoted', 'changed_to_up'] else None
            })
        
        return redirect('post_detail', post_id=post.pk)
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=400)
        messages.error(request, f'Error: {str(e)}')
        return redirect('post_detail', post_id=post_id)


@login_required(login_url='login')
@require_POST
def downvote_post(request, post_id):
    """Disminuir votos en un post (un voto por usuario, toggle)"""
    try:
        post = get_object_or_404(Post, pk=post_id)
        user_profile = request.user.profile

        existing_vote = Vote.objects.filter(user=user_profile, post=post).first()

        if existing_vote:
            if existing_vote.vote_type == 'down':
                existing_vote.delete()
                post.downvotes = max(0, post.downvotes - 1)
                post.author.popularity_score = max(0, post.author.popularity_score + 5)
                vote_action = 'removed'
            else:
                existing_vote.vote_type = 'down'
                existing_vote.save()
                post.downvotes += 1
                post.upvotes = max(0, post.upvotes - 1)
                post.author.popularity_score = max(0, post.author.popularity_score - 15)
                vote_action = 'changed_to_down'
        else:
            Vote.objects.create(user=user_profile, post=post, vote_type='down')
            post.downvotes += 1
            post.author.popularity_score = max(0, post.author.popularity_score - 5)
            vote_action = 'downvoted'

        post.author.save()
        post.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'upvotes': post.upvotes,
                'downvotes': post.downvotes,
                'author_score': post.author.popularity_score,
                'action': vote_action,
                'user_vote': 'down' if vote_action in ['downvoted', 'changed_to_down'] else None
            })

        return redirect('post_detail', post_id=post.pk)
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=400)
        messages.error(request, f'Error: {str(e)}')
        return redirect('post_detail', post_id=post_id)


@login_required(login_url='login')
def edit_post(request, post_id):
    """Editar un post existente"""
    try:
        post = get_object_or_404(Post, pk=post_id)
        
        if post.author != request.user.profile:
            messages.error(request, 'No tienes permiso para editar este post.')
            return redirect('post_detail', post_id=post.pk)
        
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                form.save_m2m()
                
                # Guardar imágenes adicionales (galería)
                gallery_images = request.FILES.getlist('gallery')
                for img in gallery_images:
                    PostImage.objects.create(post=post, image=img)
                
                messages.success(request, 'Post actualizado.')
                return redirect('post_detail', post_id=post.pk)
        else:
            form = PostForm(instance=post)
        
        return render(request, 'social/edit_post.html', {'form': form, 'post': post})
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('home')


@login_required(login_url='login')
def delete_post(request, post_id):
    """Eliminar un post"""
    try:
        post = get_object_or_404(Post, pk=post_id)
        
        if post.author != request.user.profile:
            messages.error(request, 'No tienes permiso para eliminar este post.')
            return redirect('post_detail', post_id=post.pk)
        
        if request.method == 'POST':
            post.delete()
            messages.success(request, 'Post eliminado.')
            return redirect('home')
        
        return render(request, 'social/confirm_delete.html', {'post': post})
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('home')


@login_required(login_url='login')
@require_POST
def toggle_favorite_post(request, post_id):
    """Agregar/quitar post de favoritos"""
    post = get_object_or_404(Post, pk=post_id)
    user_profile = request.user.profile
    fav, created = Favorite.objects.get_or_create(user=user_profile, post=post)
    if not created:
        fav.delete()
        is_fav = False
    else:
        is_fav = True
        create_notification(
            recipient=post.author.user,
            sender=request.user,
            notification_type='like',
            title='Guardaron tu publicación en favoritos',
            message=f'{request.user.profile.business_name or request.user.username} guardó tu publicación en favoritos',
            related_object_id=post.id,
            related_object_type='post',
        )
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_fav, 'count': post.favorited_by.count()})
    return redirect('post_detail', post_id=post.pk)

