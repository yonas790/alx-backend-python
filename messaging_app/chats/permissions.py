from rest_framework import permissions

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
