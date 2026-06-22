from django.shortcuts import render
from django.contrib import messages
from users.models import Profile
from django.db.models import Count, Sum

def rankings(request):
    """Vista de rankings de popularidad (Leaderboard)"""
    try:
        category = request.GET.get('category', 'general')
        
        # Obtener perfiles según categoría
        if category == 'novatos':
            top_profiles = Profile.objects.filter(popularity_score__lt=1000).order_by('-popularity_score')[:50]
        elif category == 'establecidas':
            top_profiles = Profile.objects.filter(popularity_score__gte=1000).order_by('-popularity_score')[:50]
        else:
            top_profiles = Profile.objects.all().order_by('-popularity_score')[:50]
        
        # Calcular estadísticas generales
        total_companies = Profile.objects.count()
        total_posts = sum(p.posts.count() for p in top_profiles)
        
        # Si el usuario está logueado, mostrar su posición
        user_position = None
        user_profile = None
        if request.user.is_authenticated:
            try:
                user_profile = request.user.profile
                all_profiles = Profile.objects.all().order_by('-popularity_score')
                user_position = list(all_profiles).index(user_profile) + 1
                
                # Posición en categorías
                user_pos_novatos = None
                user_pos_establecidas = None
                if user_profile.popularity_score < 1000:
                    novatos = Profile.objects.filter(popularity_score__lt=1000).order_by('-popularity_score')
                    user_pos_novatos = list(novatos).index(user_profile) + 1
                else:
                    establecidas = Profile.objects.filter(popularity_score__gte=1000).order_by('-popularity_score')
                    user_pos_establecidas = list(establecidas).index(user_profile) + 1
            except (IndexError, AttributeError, ValueError):
                user_position = None
        
        # Agrupar por niveles
        tiers_count = {
            'vip': Profile.objects.filter(popularity_score__gte=5000).count(),
            'oro': Profile.objects.filter(popularity_score__gte=2500, popularity_score__lt=5000).count(),
            'plata': Profile.objects.filter(popularity_score__gte=1000, popularity_score__lt=2500).count(),
            'bronce': Profile.objects.filter(popularity_score__lt=1000).count(),
        }
        
        context = {
            'top_profiles': top_profiles,
            'user_position': user_position,
            'user_profile': user_profile,
            'total_companies': total_companies,
            'total_posts': total_posts,
            'tiers_count': tiers_count,
            'current_category': category,
        }
        
        return render(request, 'rankings/rankings.html', context)
    except Exception as e:
        messages.error(request, f'Error al cargar rankings: {str(e)}')
        return render(request, 'rankings/rankings.html', {
            'top_profiles': [],
            'user_position': None,
            'total_companies': 0,
            'total_posts': 0,
            'tiers_count': {'vip': 0, 'oro': 0, 'plata': 0, 'bronce': 0},
            'current_category': 'general',
        })
