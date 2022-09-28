from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group


class User(AbstractUser):
    profile_image = models.ImageField(upload_to='apps/static/assets/images/profile', null=True, blank=True)
    is_online = models.BooleanField(default=False)



Group.add_to_class('access_level', models.IntegerField(default=1))