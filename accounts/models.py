from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    personal_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

