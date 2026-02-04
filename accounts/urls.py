from django.urls import path

from accounts.views import GoogleLogin

urlpatterns = [
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
]