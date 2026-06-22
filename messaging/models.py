from django.db import models
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
    read_status = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"De {self.sender.business_name} a {self.recipient.business_name}"
    
    def mark_as_read(self):
        """Marca el mensaje como leído"""
        self.read_status = True
        self.save()


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

