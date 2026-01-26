# from rest_framework import serializers
#
# from notification.mails import send_welcome_email
# from user.models import User
#
#
# class RegisterNotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username','email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             **validated_data
#         )
#         send_welcome_email(user)
#         return user