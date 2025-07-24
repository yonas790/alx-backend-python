from rest_framework import permissions
from .models import Conversation

from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    Custom permission to allow only participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Explicitly check user authentication
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Allow safe methods for authenticated users, or implement more checks if needed
        return True

    def has_object_permission(self, request, view, obj):
        # obj can be Conversation or Message instance depending on the view
        # Check if user is a participant in the conversation related to the object

        user = request.user
        if not user.is_authenticated:
            return False

        # For Conversation object
        if hasattr(obj, 'participants'):
            return obj.participants.filter(pk=user.pk).exists()
        
        # For Message object: check if user is participant in message's conversation
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(pk=user.pk).exists()

        return False
    

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    ✅ Allows only participants of a conversation to access it.
    ✅ Supports read (GET), create (POST), update (PUT/PATCH), delete (DELETE).
    """

    def has_object_permission(self, request, view, obj):
        # 👇 Safe methods are usually GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS or request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # ✅ Checks if the user is part of the conversation (sender or receiver)
            return request.user == obj.sender or request.user == obj.receiver
        return False