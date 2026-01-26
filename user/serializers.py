from djoser import serializers
from djoser.serializers import UserCreateSerializer as BaseCreateUserSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

from notification.mails import send_welcome_email
from user.models import User


class UserCreateSerializer(BaseCreateUserSerializer):
    class Meta(BaseCreateUserSerializer.Meta):
        model = User
        fields = ['id','username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_welcome_email(user)
        return user

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_anonymous']
