from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.users.models import User
from django.contrib.auth.models import Group



class Image(forms.Form):
    picture = forms.ImageField()


class UserChangeForm(UserChangeForm):
    
    # profile_image = forms.ImageField()

    class Meta:
        model = User
        fields = ('profile_image',)

# 'username', 'email', 'password'