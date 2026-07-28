from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from users.models import Profile
from social.models import Post
from marketplace.models import Product, Review
from messaging.models import Conversation, Message
from notifications.models import Notification
from .serializers import (
    ProfileSerializer, PostSerializer, ProductSerializer,
    ReviewSerializer, ConversationSerializer, MessageSerializer,
    NotificationSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user.profile if hasattr(obj, 'author') else False


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all().select_related('user')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['business_name', 'bio', 'city', 'sector']


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(moderation_status='approved').select_related('author__user')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'tags__name']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        post = self.get_object()
        post.upvotes += 1
        post.save()
        return Response({'upvotes': post.upvotes, 'downvotes': post.downvotes})

    @action(detail=True, methods=['post'])
    def downvote(self, request, pk=None):
        post = self.get_object()
        post.downvotes += 1
        post.save()
        return Response({'upvotes': post.upvotes, 'downvotes': post.downvotes})

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        from social.models import Favorite
        post = self.get_object()
        profile = request.user.profile
        fav = Favorite.objects.filter(user=profile, post=post).first()
        if fav:
            fav.delete()
            return Response({'is_favorited': False})
        Favorite.objects.create(user=profile, post=post)
        return Response({'is_favorited': True})


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('user__user')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category']


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all().select_related('reviewer__user', 'seller__user')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        seller_username = self.request.query_params.get('seller')
        if seller_username:
            qs = qs.filter(seller__user__username=seller_username)
        return qs


class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Conversation.objects.none()

    def get_queryset(self):
        profile = self.request.user.profile
        return Conversation.objects.filter(
            user1=profile
        ) | Conversation.objects.filter(
            user2=profile
        )


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.none()

    def get_queryset(self):
        profile = self.request.user.profile
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            conv = Conversation.objects.filter(id=conversation_id).first()
            if conv and (conv.user1 == profile or conv.user2 == profile):
                return conv.get_messages()
        return Message.objects.filter(
            sender=profile
        ) | Message.objects.filter(
            recipient=profile
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user.profile)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.none()

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'ok'})
