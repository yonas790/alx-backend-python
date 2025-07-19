from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  

    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'full_name', 'phone_number', 'role', 'created_at']

    def get_full_name(self, obj):
        # Combines first and last name
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source='sender.email', read_only=True)  
    snippet = serializers.SerializerMethodField()  # custom message snippet

    class Meta:
        model = Message
        fields = ['message_id', 'sender_email', 'message_body', 'snippet', 'sent_at']

    def get_snippet(self, obj):
        # Return first 30 chars of message_body
        return obj.message_body[:30] + ("..." if len(obj.message_body) > 30 else "")


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def validate(self, data):
        # Example validation: must have at least 2 participants
        participants = self.initial_data.get('participants', [])
        if len(participants) < 2:
            raise serializers.ValidationError("Conversation must have at least 2 participants.")
        return data
