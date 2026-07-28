from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import KorvaAIConfig, AIConversation, AIMessage
from django.conf import settings
import google.generativeai as genai
import json

@login_required(login_url='login')
def ai_tutorial(request):
    """Tutorial de Korva IA para nuevos usuarios"""
    return render(request, 'ai/tutorial.html')


@login_required(login_url='login')
def korva_ai(request):
    """Vista principal del Asistente IA Korva"""
    try:
        profile = request.user.profile
        ai_config = profile.ai_config
        conversations = AIConversation.objects.filter(user=profile).order_by('-updated_at')[:10]
        
        # Verificar si necesita tutorial (sin API key configurada)
        needs_tutorial = not ai_config.uses_personal_key and not getattr(settings, 'GEMINI_API_KEY', None)
        
        context = {
            'ai_config': ai_config,
            'conversations': conversations,
            'needs_tutorial': needs_tutorial,
        }
        
        return render(request, 'ai/korva_ai.html', context)
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('home')


@login_required(login_url='login')
def create_conversation(request):
    """Crear una nueva conversación con IA"""
    try:
        if request.method == 'POST':
            profile = request.user.profile
            title = request.POST.get('title', 'Nueva Conversación')
            
            conversation = AIConversation.objects.create(
                user=profile,
                title=title
            )
            
            return redirect('conversation_chat', conversation_id=conversation.pk)
        
        return redirect('korva_ai')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('korva_ai')


@login_required(login_url='login')
def conversation_chat(request, conversation_id):
    """Vista para chatear en una conversación"""
    try:
        profile = request.user.profile
        conversation = AIConversation.objects.get(pk=conversation_id, user=profile)
        messages_list = conversation.messages.all().order_by('timestamp')
        ai_config = profile.ai_config
        
        context = {
            'conversation': conversation,
            'messages': messages_list,
            'ai_config': ai_config,
        }
        
        return render(request, 'ai/conversation_chat.html', context)
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('korva_ai')


@login_required(login_url='login')
@require_POST
def send_ai_message(request, conversation_id):
    """Enviar un mensaje a la IA"""
    profile = request.user.profile
    conversation = AIConversation.objects.get(pk=conversation_id, user=profile)
    ai_config = profile.ai_config
    
    content = request.POST.get('message', '').strip()
    
    if not content:
        return JsonResponse({'error': 'El mensaje no puede estar vacío'}, status=400)
    
    # Guardar mensaje del usuario
    user_message = AIMessage.objects.create(
        conversation=conversation,
        role='user',
        content=content
    )
    
    try:
        # Configurar API de Google Gemini
        if ai_config.uses_personal_key and ai_config.user_api_key:
            api_key = ai_config.user_api_key
        else:
            # Usar clave del servidor (deberías configurarla en settings)
            from django.conf import settings
            api_key = getattr(settings, 'GEMINI_API_KEY', None)
            
            if not api_key:
                raise ValueError("No hay clave de API configurada")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            'gemini-pro',
            system_instruction="""Eres Korva IA, un asistente virtual especializado en negocios y emprendimiento para PyMEs en Nicaragua. 
            SOLO puedes responder sobre: planes de negocio, marketing, finanzas, impuestos, registro de empresas, RUC, 
            estrategias de ventas, atención al cliente, productos, servicios, y temas relacionados con el mundo empresarial nicaragüense.
            
            REGLAS ESTRICTAS:
            - NO puedes insultar, usar lenguaje ofensivo o discriminatorio
            - NO puedes hablar de temas +18, sexuales, violencia, drogas, política partidista, religión
            - NO puedes hacer tareas académicas, resolver exámenes o trabajar por el usuario
            - NO puedes dar consejos médicos, legales (sin aclarar que no eres abogado) o financieros de inversión
            - Si el usuario insiste en temas no permitidos, responde amablemente que solo ayudas con temas empresariales
            - Mantén un tono profesional, amable y servicial
            - Responde SIEMPRE en español"""
        )
        
        # Construir historial de conversación
        history = []
        for msg in conversation.messages.exclude(pk=user_message.pk).order_by('timestamp'):
            history.append({
                'role': msg.role,
                'parts': [msg.content]
            })
        
        # Añadir el nuevo mensaje
        history.append({
            'role': 'user',
            'parts': [content]
        })
        
        # Obtener respuesta de IA
        chat = model.start_chat(history=history)
        response = chat.send_message(content)
        
        # Guardar respuesta de IA
        ai_response = AIMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=response.text
        )
        
        # Actualizar conversación
        conversation.updated_at = ai_response.timestamp
        conversation.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'response': response.text,
                'message_id': ai_response.pk
            })
        
        return redirect('conversation_chat', conversation_id=conversation.pk)
        
    except Exception as e:
        error_message = f"Error al procesar tu solicitud: {str(e)}"
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': error_message}, status=500)
        
        messages.error(request, error_message)
        return redirect('conversation_chat', conversation_id=conversation.pk)


@login_required(login_url='login')
def update_ai_config(request):
    """Actualizar configuración de IA del usuario"""
    if request.method == 'POST':
        profile = request.user.profile
        ai_config = profile.ai_config
        
        api_key = request.POST.get('user_api_key', '').strip()
        uses_personal_key = request.POST.get('uses_personal_key', False) == 'on'
        
        if api_key:
            ai_config.user_api_key = api_key
            ai_config.uses_personal_key = True
        else:
            ai_config.uses_personal_key = False
        
        ai_config.save()
        messages.success(request, 'Configuración de IA actualizada.')
        return redirect('korva_ai')
    
    return redirect('korva_ai')


@login_required(login_url='login')
def quick_prompts(request):
    """Prompts rápidos predefinidos para consultas comunes"""
    
    quick_prompts_list = [
        {
            'title': 'Plan de Negocio',
            'prompt': '¿Cuáles son los pasos principales para crear un plan de negocio exitoso?',
            'icon': 'fa-chart-line'
        },
        {
            'title': 'Registro RUC',
            'prompt': '¿Cómo registro mi empresa en el RUC de Nicaragua?',
            'icon': 'fa-document'
        },
        {
            'title': 'Envíos Nacionales',
            'prompt': '¿Cuáles son las mejores opciones para envíos a nivel nacional en Nicaragua?',
            'icon': 'fa-truck'
        },
        {
            'title': 'Impuestos',
            'prompt': '¿Cuáles son mis obligaciones fiscales como PyME en Nicaragua?',
            'icon': 'fa-percentage'
        },
        {
            'title': 'Marketing Digital',
            'prompt': '¿Cómo puedo mejorar mi presencia digital y alcanzar más clientes?',
            'icon': 'fa-bullhorn'
        },
        {
            'title': 'Estrategia Korva',
            'prompt': '¿Cómo puedo aprovechar al máximo la plataforma Korva para crecer?',
            'icon': 'fa-rocket'
        },
    ]
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'prompts': quick_prompts_list})
    
    return render(request, 'ai/quick_prompts.html', {'prompts': quick_prompts_list})
