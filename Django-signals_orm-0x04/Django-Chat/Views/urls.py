from django.urls import path
from .Views.views import delete_user

urlpatterns = [
    path('delete_account/', delete_user, name='delete_user'),
]
