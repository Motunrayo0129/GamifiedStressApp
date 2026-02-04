from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class SocialAccountAdapter(DefaultSocialAccountAdapter):
	def pre_social_login(self, request, sociallogin):
		email = sociallogin.user.email
	
		if not email:
			return
	
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			return
			
		sociallogin.connect(request, user)