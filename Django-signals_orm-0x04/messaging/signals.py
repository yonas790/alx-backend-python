from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Create a notification for the receiver when a new message is sent.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before saving an edited message, log its old content to MessageHistory.
    """
    if instance.pk:  # only if updating an existing message
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        # Check if the content has changed
        if old_message.content != instance.content:
            # Create a history entry
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content
            )
            # Mark the message as edited
            instance.edited = True
            instance.edited_at = timezone.now()
            # (edited_by should be set from the view that edits the message)
