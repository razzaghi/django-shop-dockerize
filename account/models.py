from enum import Enum

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


    @staticmethod
    def get_user(request):
        user = CustomUser.objects.filter(username=request.user.username).first()

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_session_key(request):
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key

class ActionType(Enum):
    Like = "Like"
    Bought = "Bought"
    Share = "Share"
    Favorite = "Favorite"
    End = "End"
    View = "View"
    Click = "Click"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class ActionsLog(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(CustomUser,blank=True,null=True,on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40,blank=True,null=True)
    ip = models.CharField(max_length=20,blank=True,null=True)
    action = models.CharField(choices=ActionType.choices(),max_length=20)
    value = models.IntegerField(default=1)

    def add_action(self,request,_action_type,_value):
        _user = CustomUser.get_user(request)
        _session_key = CustomUser.get_session_key(request)
        _ip = CustomUser.get_client_ip(request)

    @staticmethod
    def check_action():
        pass







