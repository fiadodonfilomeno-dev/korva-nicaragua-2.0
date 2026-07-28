from django.db import models
from users.models import Profile

class AnalyticsReport(models.Model):
    """Modelo para reportes analíticos de los usuarios"""
    
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='analytics_report')
    total_posts = models.IntegerField(default=0)
    total_products = models.IntegerField(default=0)
    total_collaborations = models.IntegerField(default=0)
    total_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_purchases = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    followers_growth = models.IntegerField(default=0)
    engagement_rate = models.FloatField(default=0.0)
    last_generated = models.DateTimeField(auto_now=True)
    period_month = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-last_generated']
    
    def __str__(self):
        return f"Reporte - {self.user.business_name}"

