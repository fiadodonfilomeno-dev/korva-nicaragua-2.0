from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()


@register.filter
def time_ago(value):
    """Retorna hace cuanto tiempo se creo algo (ej: hace 5 minutos)"""
    if not value:
        return ''

    now = timezone.now()
    diff = now - value

    if diff < timedelta(seconds=60):
        return 'ahora mismo'
    elif diff < timedelta(minutes=60):
        minutes = int(diff.total_seconds() / 60)
        return f'hace {minutes} min' if minutes == 1 else f'hace {minutes} mins'
    elif diff < timedelta(hours=24):
        hours = int(diff.total_seconds() / 3600)
        return f'hace {hours} hora' if hours == 1 else f'hace {hours} horas'
    elif diff < timedelta(days=7):
        days = diff.days
        return f'hace {days} dia' if days == 1 else f'hace {days} dias'
    elif diff < timedelta(days=30):
        weeks = int(diff.days / 7)
        return f'hace {weeks} semana' if weeks == 1 else f'hace {weeks} semanas'
    elif diff < timedelta(days=365):
        months = int(diff.days / 30)
        return f'hace {months} mes' if months == 1 else f'hace {months} meses'
    else:
        years = int(diff.days / 365)
        return f'hace {years} ano' if years == 1 else f'hace {years} anos'
