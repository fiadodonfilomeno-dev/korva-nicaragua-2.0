from django.db import models
from users.models import Profile


class Event(models.Model):
    """Modelo para eventos y ferias de negocios"""
    CATEGORY_CHOICES = [
        ('feria', 'Feria'),
        ('taller', 'Taller'),
        ('conferencia', 'Conferencia'),
        ('networking', 'Networking'),
        ('otro', 'Otro'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='feria')
    organizer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='organized_events')
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=300)
    city = models.CharField(max_length=50, choices=Profile.CITY_CHOICES, default='managua')
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    attendees = models.ManyToManyField(Profile, related_name='attending_events', blank=True)
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} - {self.date}"

    @property
    def attendee_count(self):
        return self.attendees.count()

    @property
    def is_full(self):
        if self.max_attendees:
            return self.attendee_count >= self.max_attendees
        return False
