from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    After a user is deleted, remove all related messages,
    notifications, and message history explicitly (if not already handled by CASCADE).
    """

    # Messages (both sent and received)
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Notifications
    Notification.objects.filter(user=instance).delete()

    # MessageHistory related to the deleted user's messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()