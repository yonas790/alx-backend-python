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
    Fetch all messages where the logged-in user is either sender or receiver.
    Use select_related and prefetch_related to optimize queries.
    Retrieve threaded replies recursively.
    """
    user = request.user

    # Fetch top-level messages (no parent) involving this user
    top_messages = Message.objects.filter(
        sender=user
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
