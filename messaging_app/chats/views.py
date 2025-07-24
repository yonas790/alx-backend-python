from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipant
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .pagination import MessagePagination
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipant]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['participants__user_id']
    search_fields = ['conversation_id', 'message_body']
    ordering_fields = ['created_at', 'sent_at']
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get('participants', [])
        if not participants_ids or len(participants_ids) < 2:
            return Response(
                {"error": "At least two participants are required to create a conversation."},
                status=status.HTTP_400_BAD_REQUEST
            )
        conversation = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participants_ids)
        conversation.participants.set(users)
        conversation.save()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipant]
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['conversation__conversation_id', 'sender__user_id']
    search_fields = ['message_body']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        # Filter messages to only those in conversations where the request user is a participant
        user = self.request.user
        # Assuming your User model is linked to request.user, else adjust accordingly
        return Message.objects.filter(conversation__participants=user)

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')

        if not conversation_id or not sender_id or not message_body:
            return Response(
                {"error": "conversation, sender, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(User, user_id=sender_id)

        # Permission check: sender must be a participant of the conversation
        if not conversation.participants.filter(pk=sender.pk).exists():
            return Response(
                {"error": "Sender must be a participant of the conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        message = self.get_object()
        # Permission check: only sender can update the message
        if message.sender != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()
        # Permission check: only sender can delete the message
        if message.sender != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)