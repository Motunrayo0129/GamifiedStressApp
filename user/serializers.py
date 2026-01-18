from djoser.serializers import UserCreateSerializer as CreateUserSerializer
from phonenumber_field.serializerfields import PhoneNumberField


class UserCreateSerializer(CreateUserSerializer):
    phone_number = PhoneNumberField()
    class Meta(CreateUserSerializer.Meta):
        fields = ['first_name', 'last_name', 'username', 'email', 'role','password', 'phone_number']
