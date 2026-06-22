from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import Profile, EmailVerificationToken
from .forms import UserRegistrationForm, ProfileUpdateForm
from social.models import Post, Comment
from marketplace.models import Product
from core.models import KorvaAIConfig

def send_verification_email(user, request):
    """Envía email de verificación al usuario"""
    token_obj, created = EmailVerificationToken.objects.get_or_create(user=user)
    if not created:
        # Regenerar token si ya existe
        import uuid
        token_obj.token = uuid.uuid4()
        token_obj.save()
    
    verification_url = f"{settings.FRONTEND_URL}/verify-email/{token_obj.token}/"
    
    subject = 'Verifica tu correo electrónico - Korva Nicaragua'
    html_message = render_to_string('auth/verification_email.html', {
        'user': user,
        'verification_url': verification_url,
        'hours': settings.EMAIL_VERIFICATION_TIMEOUT_HOURS,
    })
    
    try:
        send_mail(
            subject,
            f'Verifica tu cuenta en Korva Nicaragua: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        return False

def register(request):
    """Vista para registrar nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Crear usuario manualmente (el formulario es forms.Form, no ModelForm)
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.is_active = False  # Usuario inactivo hasta verificar email
            user.save()
            
            # Crear perfil automáticamente
            profile = Profile.objects.create(
                user=user,
                business_name=form.cleaned_data['business_name'],
                city=form.cleaned_data['city'],
                sector=form.cleaned_data['sector'],
                ruc=form.cleaned_data['ruc']
            )
            
            # Crear configuración de IA
            KorvaAIConfig.objects.create(user=profile)
            
            # Enviar email de verificación
            if send_verification_email(user, request):
                messages.success(request, 'Cuenta creada exitosamente. Hemos enviado un correo de verificación a tu email.')
            else:
                messages.warning(request, 'Cuenta creada, pero no pudimos enviar el email de verificación. Contacta a soporte.')
            
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})

def verify_email(request, token):
    """Vista para verificar el email del usuario"""
    try:
        token_obj = EmailVerificationToken.objects.get(token=token)
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'Token de verificación inválido.')
        return redirect('login')
    
    if not token_obj.is_valid():
        messages.error(request, 'El token de verificación ha expirado.')
        token_obj.delete()
        return redirect('login')
    
    user = token_obj.user
    user.is_active = True
    user.save()
    
    token_obj.delete()
    
    messages.success(request, '¡Correo verificado exitosamente! Ya puedes iniciar sesión.')
    return redirect('login')


def login_view(request):
    """Vista para iniciar sesión"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('home')


def profile_view(request, username):
    """Vista para ver el perfil de un usuario"""
    try:
        user = get_object_or_404(User, username=username)
        profile = user.profile
        
        # Obtener posts y productos del usuario
        posts = profile.posts.all()[:10]
        products = profile.products.all()[:10]
        
        context = {
            'profile': profile,
            'user_obj': user,
            'posts': posts,
            'products': products,
        }
        
        return render(request, 'users/profile.html', context)
    except Exception as e:
        messages.error(request, f'Error al cargar el perfil: {str(e)}')
        return redirect('home')


@login_required(login_url='login')
def edit_profile(request):
    """Vista para editar el perfil del usuario"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'users/edit_profile.html', {'form': form, 'profile': profile})


@login_required(login_url='login')
def dashboard(request):
    """Vista del dashboard principal del usuario"""
    profile = request.user.profile
    
    context = {
        'profile': profile,
        'total_posts': profile.posts.count(),
        'total_products': profile.products.count(),
        'followers': profile.followers_count,
        'collaborations': profile.collaborations_count,
    }
    
    return render(request, 'users/dashboard.html', context)

