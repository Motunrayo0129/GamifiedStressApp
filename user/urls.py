from django.urls import path

from user.views import MyProfile, AnonymousLogin

urlpatterns = [
    path('auth/profile/', MyProfile.as_view(), name='profile'),
    path('auth/anonymous/', AnonymousLogin.as_view(), name='anonymous login'),
]