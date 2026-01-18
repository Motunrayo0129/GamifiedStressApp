from django.urls import path

from user.views import MyProfile

urlpatterns = [
    path('auth/profile/', MyProfile.as_view(), name='profile'),
]