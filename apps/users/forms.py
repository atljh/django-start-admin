from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.models import User
from apps.users.models import User
from django.contrib.auth.models import Group


class UserChangeForm(UserChangeForm):
    groups = forms.ModelChoiceField(queryset=Group.objects.all())

    
    class Meta:
        model = User
        fields = ('image', 'username', 'email', 'password')

