from django.db import models
from users.models import Profile


class Group(models.Model):
    """Modelo para grupos por sector"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    sector = models.CharField(max_length=50, choices=Profile.SECTOR_CHOICES)
    image = models.ImageField(upload_to='groups/', null=True, blank=True)
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='admin_groups')
    members = models.ManyToManyField(Profile, related_name='groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.members.count()


class GroupPost(models.Model):
    """Posts dentro de un grupo"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='group_posts')
    content = models.TextField()
    image = models.ImageField(upload_to='groups/posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.business_name} en {self.group.name}"
