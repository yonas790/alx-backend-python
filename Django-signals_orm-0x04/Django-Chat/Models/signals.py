from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before saving an edited message, log the old content into MessageHistory.
    """
    if instance.pk:  # Update, not creation
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        # If content changed
        if old_message.content != instance.content:
            # Store the previous version in MessageHistory
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content
            )

            # Update fields for tracking
            instance.edited = True
            instance.edited_at = timezone.now()
            # instance.edited_by should be set from your view/form
