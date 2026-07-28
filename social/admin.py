from django.contrib import admin
from .models import Post, Comment, Vote, PostImage

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['author', 'content', 'timestamp']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'upvotes', 'downvotes', 'moderation_status', 'timestamp']
    list_filter = ['moderation_status', 'timestamp', 'author__sector']
    search_fields = ['title', 'content', 'author__business_name']
    actions = ['approve_posts', 'flag_posts', 'remove_posts']
    inlines = [PostImageInline, CommentInline]
    readonly_fields = ['upvotes', 'downvotes', 'timestamp', 'updated_at']
    
    def approve_posts(self, request, queryset):
        queryset.update(moderation_status='approved')
    approve_posts.short_description = "Aprobar posts seleccionados"
    
    def flag_posts(self, request, queryset):
        queryset.update(moderation_status='flagged')
    flag_posts.short_description = "Marcar posts seleccionados"
    
    def remove_posts(self, request, queryset):
        queryset.update(moderation_status='removed')
    remove_posts.short_description = "Remover posts seleccionados"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'timestamp', 'upvotes']
    list_filter = ['timestamp']
    search_fields = ['content', 'author__business_name', 'post__title']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'vote_type', 'created_at']
    list_filter = ['vote_type']
    search_fields = ['user__business_name', 'post__title']

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'uploaded_at']
