from django.db import models
from django.db.models import Q
from users.models import Profile

class Message(models.Model):
    """Modelo para mensajería privada entre usuarios"""
    
    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField(blank=True, help_text="Texto del mensaje (opcional si hay imagen/video)")
    image = models.ImageField(upload_to='messages/', null=True, blank=True)
    video = models.FileField(upload_to='messages/videos/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(Profile, related_name='read_messages', blank=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"De {self.sender.business_name} a {self.recipient.business_name}"
    
    def is_read_by(self, profile):
        """Verifica si un usuario ha leído el mensaje"""
        return self.read_by.filter(pk=profile.pk).exists()
    
    def mark_as_read(self, profile):
        """Marca el mensaje como leído por un usuario"""
        self.read_by.add(profile)
    
    @property
    def read_status(self):
        """Compatibilidad hacia atrás - True si el destinatario lo leyó"""
        return self.read_by.filter(pk=self.recipient.pk).exists()


class Conversation(models.Model):
    """Modelo para mantener track de conversaciones entre usuarios"""
    
    user1 = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='conversations_as_user1'
    )
    user2 = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='conversations_as_user2'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversación: {self.user1.business_name} <-> {self.user2.business_name}"
    
    def get_other_user(self, profile):
        """Obtiene el otro usuario en la conversación"""
        return self.user2 if self.user1 == profile else self.user1
    
    def get_messages(self):
        """Obtiene todos los mensajes de la conversación"""
        return Message.objects.filter(
            models.Q(sender=self.user1, recipient=self.user2) |
            models.Q(sender=self.user2, recipient=self.user1)
        ).order_by('timestamp')

