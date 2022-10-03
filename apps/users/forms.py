from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.users.models import User
from django.contrib.auth.models import Group
from django.forms import ModelForm


class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = (
                'username',
                'email',
                )