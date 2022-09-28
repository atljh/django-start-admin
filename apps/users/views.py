import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from .forms import UserChangeForm, Image
from apps.home.models import Modul
from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.http import JsonResponse


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):    
    user.is_online = True
    user.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.is_online = False
    user.save()


def is_moderator(user):
    return user.groups.filter(name='Moderator').exists()

def is_administrator(user):
    return user.groups.filter(name='Administrator').exists()


@login_required(login_url="/login/")
def users_observe(request):
    users = User.objects.all()
    context = {
        'users': users,
    }

    return render(request, 'users/users-observe.html', context=context)


@login_required(login_url="/login/")
def users_control(request):

    if request.method == 'POST':
        group = request.POST.get('group')
        print(request.POST)
        return redirect('/users-control/')

    else:
        groups = Group.objects.all()
        moduls = Modul.objects.all()

        context = {
            'groups': groups,
            'moduls': moduls

        }
        return render(request, 'users/users-control.html', context=context)


@login_required(login_url="/login/")
def change_modul_accces(request):
    group_obj = Group.objects.get(name=request.POST.get('group'))
    modul_obj = Modul.objects.get(name=request.POST.get('modul'))
    modul_obj.access_level = group_obj.access_level
    modul_obj.save()
    return JsonResponse({'response': 'success'})


@login_required(login_url="/login/")
def logs(request):
    context = {}
    return render(request, 'users/logs.html', context=context)


@login_required(login_url="/login/")
def profile(request):
    if request.method == "POST":
        user = User.objects.get(id = request.user.id)
        if len(request.FILES) != 0:
            user.profile_image = request.FILES['profile_image']
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()

        return redirect('/')
    else:
        
        user = request.user
        groups = Group.objects.all()
        form = UserChangeForm()

        context = {
            'groups': groups,
            'user_obj': user,
            'form': form,
        }
        return render(request, 'users/profile.html', context=context)


@login_required(login_url="/login/")
def user(request, user_id):
        if not request.user.groups.first().access_level >= 3:
            return redirect('/')
        if request.method == "POST":
            user = User.objects.get(id = user_id)
            if len(request.FILES) != 0:
                user.profile_image = request.FILES['profile_image']
            if request.POST.get('group'):
                group = Group.objects.get(name=request.POST.get('group'))
                user.groups.clear()
                user.groups.add(group)
            user.username = request.POST.get('username', user.username)
            user.email = request.POST.get('email', user.email)
            user.save()

            return redirect('/users/')
        else:
            user_obj = User.objects.get(id=user_id)
            groups = Group.objects.all()
            context = {
                'groups': groups,
                'user_obj': user_obj,
            }
            return render(request, 'users/profile.html', context=context)

