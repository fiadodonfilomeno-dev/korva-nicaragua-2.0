from django.contrib import admin
from .models import KorvaAIConfig, AIConversation, AIMessage

class AIMessageInline(admin.TabularInline):
    model = AIMessage
    extra = 0
    readonly_fields = ['role', 'content', 'timestamp']

@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['title', 'user__business_name']
    inlines = [AIMessageInline]

@admin.register(KorvaAIConfig)
class KorvaAIConfigAdmin(admin.ModelAdmin):
    list_display = ['user', 'uses_personal_key']
    search_fields = ['user__business_name']

@admin.register(AIMessage)
class AIMessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'content', 'timestamp']
    list_filter = ['role', 'timestamp']
    search_fields = ['content']
