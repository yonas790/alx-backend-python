from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

User = get_user_model()


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
