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
    def likes_count(self):
        return 0

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


class ProductFavorite(models.Model):
    """Modelo para favoritos de productos"""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favorite_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.business_name} favorito: {self.product.name}"


class Review(models.Model):
    """Modelo para calificaciones y reseñas de vendedores"""
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews_given')
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews_received')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'seller', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer.business_name} -> {self.seller.business_name}: {self.rating}★"


class Deal(models.Model):
    """Modelo para ofertas y descuentos"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='deals')
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='deals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    discount_percent = models.PositiveIntegerField(help_text="Porcentaje de descuento (1-100)")
    original_price = models.DecimalField(max_digits=12, decimal_places=2)
    deal_price = models.DecimalField(max_digits=12, decimal_places=2)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.discount_percent}% OFF"

    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.ends_at

    @property
    def deal_price_display(self):
        currency_symbol = 'C$' if self.product.currency == 'NIO' else '$'
        return f"{currency_symbol} {self.deal_price:,.2f}"

