from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True)
    balance = models.IntegerField()

    USERNAME_FIELD = "username"
