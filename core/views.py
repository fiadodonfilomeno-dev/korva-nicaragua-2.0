from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from users.models import Profile
from users.report_views import get_blocked_user_ids


def search(request):
    """Busqueda avanzada unificada"""
    q = request.GET.get('q', '').strip()
    section = request.GET.get('section', 'all')
    results = {'profiles': [], 'posts': [], 'products': [], 'groups': []}
    blocked = get_blocked_user_ids(request.user) if request.user.is_authenticated else set()

    if q:
        from social.models import Post
        from marketplace.models import Product
        from groups.models import Group

        if section in ('all', 'profiles'):
            results['profiles'] = Profile.objects.exclude(
                user__in=blocked
            ).filter(
                Q(business_name__icontains=q) | Q(bio__icontains=q) | Q(city__icontains=q) | Q(sector__icontains=q)
            )[:20]

        if section in ('all', 'posts'):
            results['posts'] = Post.objects.filter(
                moderation_status='approved'
            ).exclude(
                author__user__in=blocked
            ).filter(
                Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)
            ).distinct()[:20]

        if section in ('all', 'products'):
            results['products'] = Product.objects.filter(is_active=True).exclude(
                user__user__in=blocked
            ).filter(
                Q(name__icontains=q) | Q(description__icontains=q)
            )[:20]

        if section in ('all', 'groups'):
            results['groups'] = Group.objects.exclude(
                created_by__user__in=blocked
            ).filter(
                Q(name__icontains=q) | Q(description__icontains=q) | Q(sector__icontains=q)
            )[:20]

    total = sum(len(v) for v in results.values())
    sections = [('all', 'Todos'), ('profiles', 'Empresas'), ('posts', 'Publicaciones'), ('products', 'Productos'), ('groups', 'Grupos')]
    context = {'q': q, 'section': section, 'results': results, 'total': total, 'sections': sections}
    return render(request, 'core/search.html', context)


def compute_relevance(profile, user_profile=None):
    """Calcula un score de compatibilidad entre dos perfiles"""
    score = 0
    reasons = []

    if not user_profile:
        return score, reasons

    # Misma ciudad: +30
    if profile.city == user_profile.city:
        score += 30
        reasons.append('Misma ciudad')

    # Mismo sector: +40
    if profile.sector == user_profile.sector:
        score += 40
        reasons.append('Mismo sector')

    # Tags en comun entre posts: +15 por tag compartido
    user_tags = set(
        t.name for p in user_profile.posts.all()
        for t in p.tags.all()
    )
    profile_tags = set(
        t.name for p in profile.posts.all()
        for t in p.tags.all()
    )
    shared_tags = user_tags & profile_tags
    if shared_tags:
        score += min(len(shared_tags) * 15, 45)
        reasons.append(f'Tags: {", ".join(list(shared_tags)[:3])}')

    # Productos en la misma categoria: +20
    user_cats = set(user_profile.products.values_list('category', flat=True))
    profile_cats = set(profile.products.values_list('category', flat=True))
    shared_cats = user_cats & profile_cats
    if shared_cats:
        score += 20
        reasons.append('Venden productos similares')

    # Perfil verificado: +10
    if profile.verified:
        score += 10
        reasons.append('Verificado')

    # Proximidad de popularidad: hasta +10
    diff = abs(profile.popularity_score - user_profile.popularity_score)
    if diff < 500:
        score += 10
    elif diff < 2000:
        score += 5

    return score, reasons


@login_required(login_url='login')
def recommendations(request):
    """Muestra empresas recomendadas para alianzas"""
    user_profile = request.user.profile

    # Obtener todos los perfiles excepto el propio
    all_profiles = Profile.objects.exclude(pk=user_profile.pk).select_related('user')

    # Calcular score para cada perfil
    scored = []
    for profile in all_profiles:
        score, reasons = compute_relevance(profile, user_profile)
        if score > 0:
            scored.append({
                'profile': profile,
                'score': score,
                'reasons': reasons,
            })

    # Ordenar por score descendente
    scored.sort(key=lambda x: x['score'], reverse=True)

    # Top 20 recomendaciones
    recommendations_list = scored[:20]

    # Filtro por sector
    sector_filter = request.GET.get('sector')
    if sector_filter:
        recommendations_list = [
            r for r in recommendations_list
            if r['profile'].sector == sector_filter
        ]

    context = {
        'recommendations': recommendations_list,
        'user_profile': user_profile,
        'sector_filter': sector_filter,
        'sectors': Profile.SECTOR_CHOICES,
    }

    return render(request, 'core/recommendations.html', context)


def activity_feed(request):
    """Feed unificado de actividad reciente en la plataforma"""
    from social.models import Post
    from marketplace.models import Product, Review
    from events.models import Event

    blocked = get_blocked_user_ids(request.user) if request.user.is_authenticated else set()

    activities = []

    # Posts
    for p in Post.objects.filter(moderation_status='approved').exclude(author__user__in=blocked).select_related('author__user')[:30]:
        activities.append({
            'type': 'post',
            'actor': p.author,
            'actor_username': p.author.user.username,
            'title': p.title,
            'description': p.content[:200],
            'image': p.image.url if p.image else None,
            'url': f'/post/{p.id}/',
            'timestamp': p.timestamp,
            'icon': 'fa-newspaper',
            'color': 'text-blue-400',
        })

    # Products
    for p in Product.objects.filter(is_active=True).exclude(user__user__in=blocked).select_related('user__user')[:30]:
        activities.append({
            'type': 'product',
            'actor': p.user,
            'actor_username': p.user.user.username,
            'title': p.name,
            'description': f'{p.get_currency_display()} {p.price}',
            'image': p.image.url if p.image else None,
            'url': f'/product/{p.id}/',
            'timestamp': p.created_at,
            'icon': 'fa-tag',
            'color': 'text-korva-success',
        })

    # Reviews
    for r in Review.objects.exclude(reviewer__user__in=blocked).select_related('reviewer__user', 'seller__user')[:30]:
        stars = '&#9733;' * r.rating + '&#9734;' * (5 - r.rating)
        activities.append({
            'type': 'review',
            'actor': r.reviewer,
            'actor_username': r.reviewer.user.username,
            'title': f'Resena para {r.seller.business_name}',
            'description': f'{"&#9733;" * r.rating}{"&#9734;" * (5 - r.rating)} {r.comment[:200]}' if r.comment else f'{"&#9733;" * r.rating}',
            'image': None,
            'url': f'/reviews/{r.seller.user.username}/',
            'timestamp': r.created_at,
            'icon': 'fa-star',
            'color': 'text-yellow-400',
        })

    # Events
    for e in Event.objects.filter(is_active=True).exclude(organizer__user__in=blocked).select_related('organizer__user')[:30]:
        activities.append({
            'type': 'event',
            'actor': e.organizer,
            'actor_username': e.organizer.user.username,
            'title': e.title,
            'description': f'{e.get_category_display()} - {e.city} - {e.date}',
            'image': e.image.url if hasattr(e, 'image') and e.image else None,
            'url': f'/events/{e.id}/',
            'timestamp': e.created_at,
            'icon': 'fa-calendar-alt',
            'color': 'text-purple-400',
        })

    activities.sort(key=lambda a: a['timestamp'], reverse=True)

    context = {
        'activities': activities[:50],
        'total': len(activities[:50]),
    }
    return render(request, 'core/activity_feed.html', context)
