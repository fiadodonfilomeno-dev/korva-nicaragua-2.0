from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile
from social.models import Post
from marketplace.models import Product, Review
from messaging.models import Message, Conversation
from notifications.models import Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    city_display = serializers.SerializerMethodField()
    sector_display = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'business_name', 'logo', 'banner', 'bio', 'city', 'city_display', 'sector', 'sector_display', 'verified', 'popularity_score', 'created_at']

    def get_city_display(self, obj):
        return obj.get_city_display()

    def get_sector_display(self, obj):
        return obj.get_sector_display()


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    author_name = serializers.CharField(source='author.business_name', read_only=True)
    tags_list = serializers.ListField(source='tags.names', read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'title', 'content', 'image', 'video', 'timestamp', 'updated_at', 'upvotes', 'downvotes', 'tags_list', 'moderation_status', 'is_favorited']

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and hasattr(request.user, 'profile'):
            return obj.favorited_by.filter(user=request.user.profile).exists()
        return False


class ProductSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    user_name = serializers.CharField(source='user.business_name', read_only=True)
    price_display = serializers.CharField(source='price_display', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'user', 'user_name', 'name', 'description', 'price', 'price_display', 'currency', 'category', 'image', 'contact_whatsapp', 'is_active', 'views_count', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = ProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'seller', 'product', 'rating', 'comment', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.business_name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.business_name', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'recipient', 'recipient_name', 'content', 'image', 'video', 'timestamp', 'read_by']


class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'other_user', 'last_message', 'created_at', 'updated_at']

    def get_other_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            other = obj.get_other_user(request.user.profile) if hasattr(request.user, 'profile') else None
            if other:
                return ProfileSerializer(other).data
        return None

    def get_last_message(self, obj):
        msg = obj.get_messages().last()
        if msg:
            return MessageSerializer(msg).data
        return None


class NotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True, default=None)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'sender', 'sender_name', 'notification_type', 'title', 'message', 'related_object_id', 'related_object_type', 'is_read', 'created_at']
