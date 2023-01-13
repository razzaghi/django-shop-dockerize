from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    self_registered = models.BooleanField(default=False)
    ip = models.CharField(max_length=200, blank=True)
    session_key = models.CharField(max_length=200, blank=True)






