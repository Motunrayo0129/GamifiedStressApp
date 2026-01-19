from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = PhoneNumberField(region='NG' ,unique=True, blank=True, null=True)
    is_anonymous = models.BooleanField(default=False)




