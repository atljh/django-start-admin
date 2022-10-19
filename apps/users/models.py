from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.core.cache import cache 
import datetime
from core import settings


class User(AbstractUser):
    profile_image = models.ImageField(upload_to='apps/static/assets/images/profile', null=True, blank=True)
    is_online = models.BooleanField(default=False)
    timezone = models.CharField(max_length=100, default='UTC')

    def last_seen(self):
        return cache.get('seen_%s' % self.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                        seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False 



Group.add_to_class('access_level', models.IntegerField(default=1))