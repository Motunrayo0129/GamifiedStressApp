from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT','student'
        WORKER = 'WORKER','worker'
        INDIVIDUAL = 'INDIVIDUAL', 'Individual'
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(region='NG' ,unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)





