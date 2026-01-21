from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.utilities import generate_random_string

# Create your views here.
User = get_user_model()

class MyProfile(APIView):
	permission_classes = [AllowAny]
	def get(self, request):
		user = request.user
		if user.is_anonymous:
			return Response({
				'id': user.id,
				'username': user.username,
			})
		else:
			return Response({
				'id': user.id,
				'username': user.username,
				'email': user.email,
			})

@api_view(['POST'])
@permission_classes([AllowAny])
def anonymous_login(request):
	user = User.objects.create(
		username=f"anon{generate_random_string(9)}{User.objects.count() + 1}",
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