from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()


class NotificationSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="pass")
        self.receiver = User.objects.create_user(username="bob", password="pass")

    def test_notification_created_on_message(self):
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello Bob!"
        )
        notif = Notification.objects.filter(user=self.receiver, message=msg).first()
        self.assertIsNotNone(notif)
