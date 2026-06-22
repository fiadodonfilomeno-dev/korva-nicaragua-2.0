from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Notification(models.Model):
    """Modelo para notificaciones del sistema"""
    
    TYPE_CHOICES = [
        ('message', 'Nuevo Mensaje'),
        ('like', 'Like en tu publicación'),
        ('comment', 'Comentario en tu publicación'),
        ('follow', 'Nuevo seguidor'),
        ('product_inquiry', 'Consulta de producto'),
        ('mention', 'Mención'),
        ('system', 'Notificación del sistema'),
    ]
    
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='sent_notifications'
    )
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['recipient', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.notification_type} para {self.recipient.username}"
    
    @property
    def icon(self):
        icons = {
            'message': 'fas fa-envelope',
            'like': 'fas fa-thumbs-up',
            'comment': 'fas fa-comment',
            'follow': 'fas fa-user-plus',
            'product_inquiry': 'fas fa-shopping-bag',
            'mention': 'fas fa-at',
            'system': 'fas fa-bell',
        }
        return icons.get(self.notification_type, 'fas fa-bell')


class NotificationPreference(models.Model):
    """Preferencias de notificación por usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_messages = models.BooleanField(default=True)
    email_likes = models.BooleanField(default=True)
    email_comments = models.BooleanField(default=True)
    email_follows = models.BooleanField(default=True)
    email_product_inquiries = models.BooleanField(default=True)
    email_mentions = models.BooleanField(default=True)
    email_system = models.BooleanField(default=True)
    push_messages = models.BooleanField(default=True)
    push_likes = models.BooleanField(default=True)
    push_comments = models.BooleanField(default=True)
    push_follows = models.BooleanField(default=True)
    push_product_inquiries = models.BooleanField(default=True)
    push_mentions = models.BooleanField(default=True)
    push_system = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Preferencias de {self.user.username}"