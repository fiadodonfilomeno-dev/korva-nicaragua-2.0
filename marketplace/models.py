from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from users.models import Profile


# Comision de Korva sobre transacciones (5% por defecto)
KORVA_COMMISSION_PERCENT = 5


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
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text='URL de imagen externa (Google/Unsplash)')
    contact_whatsapp = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{8,15}$',
                message='Número de WhatsApp inválido (ej: +50587654321)'
            )
        ],
        help_text="Ej: +50587654321"
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


class BankAccount(models.Model):
    """Cuenta bancaria del vendedor para recibir pagos"""
    
    BANK_CHOICES = [
        ('lafise', 'Lafise Bancentro'),
        ('banpro', 'Banpro Grupo Promerica'),
        ('bac', 'BAC Credomatic'),
    ]
    
    ACCOUNT_TYPE_CHOICES = [
        ('monetaria', 'Cuenta Monetaria'),
        ('ahorro', 'Cuenta de Ahorro'),
    ]
    
    seller = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='bank_account')
    bank = models.CharField(max_length=20, choices=BANK_CHOICES)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='monetaria')
    account_number = models.CharField(max_length=30)
    account_holder = models.CharField(max_length=200)
    id_number = models.CharField(max_length=20, help_text="Cédula o RUC del titular")
    phone = models.CharField(max_length=15, blank=True, help_text="Teléfono registrado en el banco")
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_bank_display()} - {self.account_number}"


class Transaction(models.Model):
    """Transaccion de compra-venta con comision de Korva"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente de Pago'),
        ('paid', 'Pagado (por confirmar)'),
        ('confirmed', 'Confirmado por el Vendedor'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
        ('disputed', 'En Disputa'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sales')
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Total de la transaccion")
    currency = models.CharField(max_length=3, choices=Product.CURRENCY_CHOICES, default='NIO')
    commission_percent = models.DecimalField(max_digits=5, decimal_places=2, default=KORVA_COMMISSION_PERCENT)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Comision de Korva")
    seller_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Monto para el vendedor (total - comision)")
    reference = models.CharField(max_length=20, unique=True, help_text="Referencia unica de pago")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    bank = models.CharField(max_length=20, choices=BankAccount.BANK_CHOICES, blank=True, help_text="Banco usado para el pago")
    payment_date = models.DateTimeField(null=True, blank=True)
    buyer_notes = models.TextField(blank=True, help_text="Notas del comprador al realizar el pago")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.reference} - {self.product.name} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.reference:
            import uuid
            self.reference = f"KORVA-{uuid.uuid4().hex[:8].upper()}"
        if not self.commission_amount:
            self.commission_amount = round(self.amount * self.commission_percent / 100, 2)
        if not self.seller_amount:
            self.seller_amount = self.amount - self.commission_amount
        super().save(*args, **kwargs)

    @property
    def amount_display(self):
        symbol = 'C$' if self.currency == 'NIO' else '$'
        return f"{symbol} {self.amount:,.2f}"

    @property
    def commission_display(self):
        symbol = 'C$' if self.currency == 'NIO' else '$'
        return f"{symbol} {self.commission_amount:,.2f}"

    @property
    def seller_amount_display(self):
        symbol = 'C$' if self.currency == 'NIO' else '$'
        return f"{symbol} {self.seller_amount:,.2f}"


class PayoutRequest(models.Model):
    """Solicitud de retiro de fondos del vendedor"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'En Proceso'),
        ('completed', 'Completado'),
        ('rejected', 'Rechazado'),
    ]
    
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='payout_requests')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payout {self.seller.business_name} - C${self.amount:,.2f}"

