from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from users.models import Profile

class Product(models.Model):
    """Modelo para productos en el catálogo del Marketplace"""
    
    CATEGORY_CHOICES = [
        ('ventas', 'Ventas'),
        ('compras', 'Compras'),
    ]
    
    CURRENCY_CHOICES = [
        ('NIO', 'C$ Córdobas'),
        ('USD', '$ Dólares US'),
    ]
    
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NIO')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/')
    contact_whatsapp = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Número de WhatsApp inválido'
            )
        ],
        help_text="Ej: +50587654321 o 87654321"
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.business_name}"
    
    @property
    def whatsapp_message_url(self):
        """Genera URL para enviar mensaje directo en WhatsApp"""
        # Formatear número sin espacios ni caracteres especiales
        phone = self.contact_whatsapp.replace('+', '').replace(' ', '').replace('-', '')
        message = f"Hola, estoy interesado en: {self.name} de {self.user.business_name}"
        return f"https://wa.me/{phone}?text={message}"
    
    @property
    def price_display(self):
        """Retorna el precio formateado con la moneda"""
        currency_symbol = 'C$' if self.currency == 'NIO' else '$'
        return f"{currency_symbol} {self.price:,.2f}"

