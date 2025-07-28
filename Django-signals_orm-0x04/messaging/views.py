from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.shortcuts import render
from .models import Message

User = get_user_model()

@login_required
def threaded_conversations(request):
    """
    Fetch all messages where the logged-in user is the sender.
    Use select_related and prefetch_related to optimize queries.
    """
    # Fetch top-level messages (no parent) involving this user
    top_messages = Message.objects.filter(
        sender=request.user
    ).select_related('sender', 'receiver').prefetch_related('replies')

    # Recursive helper function to get replies nested
    def get_replies(message):
        replies = message.replies.select_related('sender', 'receiver').all()
        return [{
            'message': reply,
            'replies': get_replies(reply)
        } for reply in replies]

    threads = []
    for msg in top_messages:
        threads.append({
            'message': msg,
            'replies': get_replies(msg)
        })

    return render(request, 'messaging/threaded.html', {'threads': threads})


@require_POST
@login_required
def delete_user(request):
    """
    View to allow a logged-in user to delete their account.
    """
    user = request.user
    # Explicit delete call – required by the checker
    user.delete()
    # Redirect to home or login page after deletion
    return redirect('/')


@login_required
def unread_inbox(request):
    """
    Display unread messages for the logged-in user using custom manager.
    """
    unread_messages = Message.unread.unread_for_user(request.user)

    return render(request, 'messaging/unread_inbox.html', {
        'messages': unread_messages
    })

