from django.urls import path

from user.views import MyProfile, anonymous_login

urlpatterns = [
    path('auth/profile/', MyProfile.as_view(), name='profile'),
    path('auth/anonymous/', anonymous_login, name='anonymous login'),
]