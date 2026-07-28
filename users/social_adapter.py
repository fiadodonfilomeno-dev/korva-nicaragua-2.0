from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User


class KorvaSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Adapter personalizado para crear Profile al registrar con redes sociales"""
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        # Crear Profile si no existe
        if not hasattr(user, 'profile'):
            from users.models import Profile
            from core.models import KorvaAIConfig
            
            extra_data = sociallogin.account.extra_data
            
            # Intentar obtener datos del perfil social
            business_name = extra_data.get('name', '') or extra_data.get('first_name', '') or user.username
            city = 'managua'
            sector = 'comercio'
            
            profile = Profile.objects.create(
                user=user,
                business_name=business_name,
                city=city,
                sector=sector,
                bio=extra_data.get('bio', ''),
            )
            
            # Crear configuración de IA
            KorvaAIConfig.objects.create(user=profile)
        
        return user
