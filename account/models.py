from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    self_registered = models.BooleanField(default=False)
    ip = models.CharField(max_length=200, blank=True)
    session_key = models.CharField(max_length=200, blank=True)

    @staticmethod
    def get_or_register_user(ip,session_key):
        user_ = CustomUser.objects.filter(ip=ip,session_key=session_key).first()
        if user_:
            return user_
        else:
            return CustomUser.objects.create_user(username=f'{session_key}_{ip}'.replace('.', '_'),ip=ip,session_key=session_key)




