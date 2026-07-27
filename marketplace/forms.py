from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """Formulario para crear y editar productos"""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'currency', 'category', 'image', 'contact_whatsapp']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'korva-input w-full',
                'placeholder': 'Nombre del producto o servicio',
                'maxlength': '300'
            }),
            'description': forms.Textarea(attrs={
                'class': 'korva-input w-full',
                'placeholder': 'Describe detalladamente tu producto o servicio',
                'rows': 6
            }),
            'price': forms.NumberInput(attrs={
                'class': 'korva-input w-full',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'currency': forms.Select(attrs={
                'class': 'korva-input w-full'
            }),
            'category': forms.Select(attrs={
                'class': 'korva-input w-full'
            }),
            'image': forms.FileInput(attrs={
                'class': 'block w-full text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-korva-success file:text-white hover:file:bg-green-600'
            }),
            'contact_whatsapp': forms.TextInput(attrs={
                'class': 'korva-input w-full',
                'placeholder': '+50587654321',
            }),
        }
