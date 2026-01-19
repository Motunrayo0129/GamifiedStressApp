from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
User = get_user_model()

class MyProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })


class AnonymousProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
        })

@api_view(['POST'])
def anonymous_login(request):
    user = User.objects.create(
        username=f"anonymous_{User.objects.count() + 1}",
        is_anonymous=True,
    )

    user.set_unusable_password()
    user.save()
    refresh = RefreshToken.for_user(user)

    return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'is_anonymous': user.is_anonymous
    })

