from django.conf import settings


def i18n_processor(request):
    return {
        'LANGUAGES': settings.LANGUAGES,
        'LANGUAGE_CODE': request.LANGUAGE_CODE if hasattr(request, 'LANGUAGE_CODE') else settings.LANGUAGE_CODE,
    }

def social_providers_processor(request):
    providers = []
    for provider, config in settings.SOCIALACCOUNT_PROVIDERS.items():
        app = config.get('APP', {})
        if app.get('client_id') and app.get('secret'):
            providers.append(provider)
    return {'enabled_providers': providers}
