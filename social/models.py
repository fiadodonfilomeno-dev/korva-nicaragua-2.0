from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from users.models import Profile
from taggit.managers import TaggableManager

class Post(models.Model):
    """Modelo para publicaciones en el Muro Social"""
    
    MODERATION_STATUS_CHOICES = [
        ('approved', 'Aprobado'),
        ('flagged', 'Marcado'),
        ('removed', 'Removido'),
    ]
    
    title = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True, help_text="Imagen opcional para la publicación")
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True, help_text="Video opcional para la publicación")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    upvotes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    downvotes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    moderation_status = models.CharField(
        max_length=20,
        choices=MODERATION_STATUS_CHOICES,
        default='approved'
    )
    moderation_reason = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.title} by {self.author.business_name}"
    
    def upvote(self, user_profile=None):
        """Incrementa upvotes y suma puntos de reputación al autor"""
        self.upvotes += 1
        self.author.popularity_score += 10
        self.author.save()
        self.save()
    
    def downvote(self, user_profile=None):
        """Incrementa downvotes y resta puntos de reputación al autor"""
        self.downvotes += 1
        self.author.popularity_score = max(0, self.author.popularity_score - 5)
        self.author.save()
        self.save()


class PostImage(models.Model):
    """Modelo para múltiples imágenes en un post (galería)"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"Imagen de {self.post.title}"


class Vote(models.Model):
    """Modelo para rastrear votos de usuarios (un voto por usuario por post)"""
    
    VOTE_CHOICES = [
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ]
    
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=4, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.business_name} - {self.vote_type} - {self.post.title}"


class Comment(models.Model):
    """Modelo para comentarios en posts"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    downvotes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Comentario de {self.author.business_name} en {self.post.title}"

