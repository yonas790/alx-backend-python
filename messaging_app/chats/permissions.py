from rest_framework import permissions
from .models import Conversation

class IsParticipant(permissions.BasePermission):
    """
    Custom permission: Only allow users to access messages or conversations they are part of.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
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