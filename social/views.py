from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Post, Comment, PostImage, Vote
from .forms import PostForm, CommentForm, PostImageForm
from users.models import Profile

def home(request):
    """
    MURO SOCIAL / PÁGINA DE INICIO:
    Si el usuario no está autenticado, renderiza la página de bienvenida (Landing).
    Si está autenticado, muestra el muro social con todas las publicaciones.
    Permite filtrar/buscar publicaciones por título, contenido o nombre de la PyME.
    """
    if not request.user.is_authenticated:
        return render(request, 'landing.html')
    
    try:
        posts = Post.objects.select_related('author').all()
        
        # Buscar posts
        search_query = request.GET.get('q')
        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__business_name__icontains=search_query)
            )
        
        context = {
            'posts': posts,
            'search_query': search_query,
        }
        
        return render(request, 'social/home.html', context)
    except Exception as e:
        messages.error(request, f'Error al cargar el muro: {str(e)}')
        return redirect('home')


@login_required(login_url='login')
def create_post(request):
    """
    CREAR PUBLICACIÓN:
    Permite a una PyME publicar un post con texto, etiquetas y múltiples fotos (galería).
    Asocia automáticamente la publicación al perfil del usuario logueado.
    """
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
    """
    DETALLE DE PUBLICACIÓN Y COMENTARIOS:
    Muestra la información completa de una publicación con su galería y comentarios.
    Si el usuario está autenticado, permite enviar nuevos comentarios al post.
    """
    try:
        post = get_or_404(Post, pk=post_id)
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
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('home')


@login_required(login_url='login')
@require_POST
def upvote_post(request, post_id):
    """
    VOTO POSITIVO (UPVOTE):
    Permite dar un voto de apoyo a una publicación (+10 puntos de popularidad para la PyME autora).
    Evita votos duplicados del mismo usuario (los alterna o elimina si ya existían).
    """
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
    """
    VOTO NEGATIVO (DOWNVOTE):
    Registra votos negativos reduciendo la popularidad de la PyME autora en -5 puntos.
    """
    try:
        post = get_object_or_404(Post, pk=post_id)
        post.downvotes += 1
        post.author.popularity_score = max(0, post.author.popularity_score - 5)
        post.author.save()
        post.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'upvotes': post.upvotes,
                'downvotes': post.downvotes,
                'author_score': post.author.popularity_score
            })
        
        return redirect('post_detail', post_id=post.pk)
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=400)
        messages.error(request, f'Error: {str(e)}')
        return redirect('post_detail', post_id=post_id)


@login_required(login_url='login')
def edit_post(request, post_id):
    """
    EDITAR PUBLICACIÓN:
    Permite al autor original modificar el contenido, título o añadir imágenes del post.
    """
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
    """
    ELIMINAR PUBLICACIÓN:
    Permite al autor borrar la publicación de forma permanente previa confirmación.
    """
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

