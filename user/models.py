from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.fields.phone_field import PhoneField


class User(AbstractUser):
    last_name = None
    first_name = None
    name = models.CharField('full name', max_length=100, blank=True)
    phone = PhoneField(blank=True, null=True)


