from django import forms
from .models import Post, Comment, PostImage

class PostForm(forms.ModelForm):
    """Formulario para crear y editar posts"""
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'korva-input w-full',
                'placeholder': 'Título de tu publicación',
                'maxlength': '300'
            }),
            'content': forms.Textarea(attrs={
                'class': 'korva-input w-full',
                'placeholder': 'Cuéntanos tu idea, requerimiento o propuesta',
                'rows': 6
            }),
            'image': forms.FileInput(attrs={
                'class': 'block w-full text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-korva-success file:text-white hover:file:bg-green-600',
                'accept': 'image/*'
            }),
            'video': forms.FileInput(attrs={
                'class': 'block w-full text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-korva-success file:text-white hover:file:bg-green-600',
                'accept': 'video/*'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'korva-input w-full',
                'placeholder': 'Etiquetas separadas por comas (ej: alianza, venta, servicios)',
                'data-role': 'tagsinput'
            }),
        }


class PostImageForm(forms.ModelForm):
    """Formulario para imágenes adicionales en un post"""
    
    class Meta:
        model = PostImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'block w-full text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-korva-success file:text-white hover:file:bg-green-600',
                'accept': 'image/*'
            }),
        }


class CommentForm(forms.ModelForm):
    """Formulario para comentar en posts"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'korva-input w-full',
                'placeholder': 'Escribe un comentario...',
                'rows': 3
            }),
        }
