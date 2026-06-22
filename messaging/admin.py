from django.contrib import admin
from .models import Message, Conversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['user1__business_name', 'user2__business_name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'content', 'timestamp', 'read_status']
    list_filter = ['read_status', 'timestamp']
    search_fields = ['content', 'sender__business_name', 'recipient__business_name']
