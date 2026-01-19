from djoser import serializers
from djoser.serializers import UserCreateSerializer as BaseCreateUserSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from phonenumber_field.serializerfields import PhoneNumberField

from user.models import User


class UserCreateSerializer(BaseCreateUserSerializer):
    class Meta(BaseCreateUserSerializer.Meta):
        model = User
        fields = ['id','username', 'email', 'password']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_anonymous']
