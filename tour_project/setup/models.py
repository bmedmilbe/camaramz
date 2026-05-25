from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser



class UserTokens(models.Model):
    email = models.EmailField(max_length=255)
    token = models.UUIDField(max_length=255)