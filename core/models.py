from django.db import models
from users.models import Profile

class KorvaAIConfig(models.Model):
    """Configuración de IA para cada usuario"""
    
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='ai_config')
    user_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Clave personal de API de Google Gemini (opcional)"
    )
    grok_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Clave personal de API de Grok/xAI (opcional)"
    )
    uses_personal_key = models.BooleanField(default=False)
    preferred_provider = models.CharField(
        max_length=20,
        choices=[('gemini', 'Google Gemini'), ('grok', 'Grok/xAI')],
        default='gemini'
    )
    seen_ai_tutorial = models.BooleanField(default=False)
    total_tokens_used = models.PositiveIntegerField(default=0)
    monthly_token_limit = models.PositiveIntegerField(default=100000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración IA de Korva"
        verbose_name_plural = "Configuraciones IA de Korva"
    
    def __str__(self):
        return f"IA Config - {self.user.business_name}"
    
    @property
    def tokens_remaining(self):
        """Tokens restantes del mes"""
        return max(0, self.monthly_token_limit - self.total_tokens_used)
    
    @property
    def tokens_percentage_used(self):
        """Porcentaje de tokens usados"""
        if self.monthly_token_limit == 0:
            return 0
        return min(100, (self.total_tokens_used / self.monthly_token_limit) * 100)
    
    def add_tokens_used(self, tokens):
        """Añadir tokens usados"""
        self.total_tokens_used += tokens
        self.save(update_fields=['total_tokens_used'])


class AIConversation(models.Model):
    """Modelo para guardar historial de conversaciones con IA"""
    
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ai_conversations')
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversación IA: {self.user.business_name}"


class AIMessage(models.Model):
    """Modelo para mensajes en conversaciones con IA"""
    
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('assistant', 'Asistente'),
    ]
    
    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    tokens_used = models.PositiveIntegerField(default=0)
    provider = models.CharField(
        max_length=20,
        choices=[('gemini', 'Google Gemini'), ('grok', 'Grok/xAI')],
        default='gemini'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Mensaje {self.role} - {self.conversation.user.business_name}"

