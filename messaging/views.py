from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Message, Conversation
from .forms import MessageForm
from users.models import Profile

@login_required(login_url='login')
def messages_view(request):
    """Vista de lista de conversaciones"""
    try:
        user_profile = request.user.profile
        
        # Obtener todas las conversaciones del usuario
        conversations = Conversation.objects.filter(
            Q(user1=user_profile) | Q(user2=user_profile)
        ).order_by('-updated_at')
        
        context = {
            'conversations': conversations,
        }
        
        return render(request, 'messaging/messages.html', context)
    except Exception as e:
        messages.error(request, f'Error al cargar mensajes: {str(e)}')
        return redirect('home')


@login_required(login_url='login')
def conversation_detail(request, conversation_id):
    """Vista de una conversación específica"""
    try:
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        user_profile = request.user.profile
        
        # Verificar permiso
        if conversation.user1 != user_profile and conversation.user2 != user_profile:
            messages.error(request, 'No tienes acceso a esta conversación.')
            return redirect('messages')
        
        # Obtener los mensajes de la conversación
        chat_messages = conversation.get_messages()
        
        # AJAX: comprobar nuevos mensajes
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            last_msg_id = request.GET.get('last_msg_id')
            if last_msg_id:
                new_messages = chat_messages.filter(id__gt=last_msg_id)
                if new_messages.exists():
                    return JsonResponse({'new_messages': True})
            return JsonResponse({'new_messages': False})
        
        # Marcar mensajes como leídos por el usuario actual
        for msg in chat_messages.filter(recipient=user_profile):
            if not msg.is_read_by(user_profile):
                msg.mark_as_read(user_profile)
        
        if request.method == 'POST':
            form = MessageForm(request.POST, request.FILES)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = user_profile
                
                # Determinar el destinatario
                if conversation.user1 == user_profile:
                    message.recipient = conversation.user2
                else:
                    message.recipient = conversation.user1
                
                message.save()
                conversation.updated_at = message.timestamp
                conversation.save()
                
                return redirect('conversation_detail', conversation_id=conversation.pk)
        else:
            form = MessageForm()
        
        # Obtener el otro usuario en la conversación
        other_user = conversation.get_other_user(user_profile)
        
        context = {
            'conversation': conversation,
            'other_user': other_user,
            'chat_messages': chat_messages,
            'form': form,
        }
        
        return render(request, 'messaging/conversation_detail.html', context)
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('messages')


@login_required(login_url='login')
def start_conversation(request, username):
    """Iniciar una nueva conversación con un usuario"""
    try:
        user_profile = request.user.profile
        recipient_user = get_object_or_404(Profile, user__username=username)
        
        if recipient_user == user_profile:
            messages.error(request, 'No puedes iniciar una conversación contigo mismo.')
            return redirect('profile', username=username)
        
        # Buscar o crear conversación
        conversation = Conversation.objects.filter(
            (Q(user1=user_profile, user2=recipient_user) |
             Q(user1=recipient_user, user2=user_profile))
        ).first()
        
        if not conversation:
            conversation = Conversation.objects.create(
                user1=user_profile,
                user2=recipient_user
            )
        
        return redirect('conversation_detail', conversation_id=conversation.pk)
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('messages')


@login_required(login_url='login')
def send_message(request):
    """Enviar un mensaje (puede ser AJAX)"""
    try:
        if request.method == 'POST':
            recipient_id = request.POST.get('recipient_id')
            content = request.POST.get('content')
            
            user_profile = request.user.profile
            recipient = get_object_or_404(Profile, pk=recipient_id)
            
            message = Message.objects.create(
                sender=user_profile,
                recipient=recipient,
                content=content
            )
            
            # Actualizar o crear conversación
            conversation = Conversation.objects.filter(
                (Q(user1=user_profile, user2=recipient) |
                 Q(user1=recipient, user2=user_profile))
            ).first()
            
            if conversation:
                conversation.updated_at = message.timestamp
                conversation.save()
            else:
                Conversation.objects.create(
                    user1=user_profile,
                    user2=recipient
                )
            
            return redirect('messages')
        
        return redirect('messages')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('messages')

