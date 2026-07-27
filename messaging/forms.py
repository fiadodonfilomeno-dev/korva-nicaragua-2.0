from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    """Formulario para enviar mensajes con soporte multimedia"""
    
    class Meta:
        model = Message
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'korva-input w-full',
                'placeholder': 'Escribe tu mensaje...',
                'rows': 2
            }),
            'image': forms.FileInput(attrs={
                'class': 'block w-full text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-korva-success file:text-white hover:file:bg-green-600',
                'accept': 'image/*'
            }),
            'video': forms.FileInput(attrs={
                'class': 'block w-full text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-korva-success file:text-white hover:file:bg-green-600',
                'accept': 'video/*'
            }),
        }
