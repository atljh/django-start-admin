from .forms import EditProfileForm
from apps.authentication.forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from apps.home.models import Module
from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from apps.home.views import module_access
from django.shortcuts import get_object_or_404


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):    
    user.is_online = True
    user.save()


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.is_online = False
    user.save()


@login_required(login_url="/login/")
def users(request):
    if not module_access(request, 'Users'):
        return redirect('/')
    users = User.objects.all()

    context = {
        'users': users,
    }

    return render(request, 'users/users-observe.html', context=context)


@login_required(login_url="/login/")
def modules(request):
    if not module_access(request, 'Users'):
        return redirect('/')
    else:
        groups = Group.objects.all()
        modules = Module.objects.all().order_by('-id')

        context = {
            'groups': groups,
            'modules': modules

        }
        return render(request, 'users/users-control.html', context=context)


@login_required(login_url="/login/")
def change_module_accces(request):
    if not module_access(request, 'Users'):
        return redirect('/')
    try:
        group_obj = Group.objects.get(name=request.POST.get('group'))
        module_obj = Module.objects.get(name=request.POST.get('module'))
        module_obj.access_level = group_obj.access_level
        module_obj.save()
        print(module_obj.name, group_obj.name)
    except Exception as exc:
        return JsonResponse({'error': f'{exc}'}, status=500)
    return JsonResponse({'response': 'success'})


@login_required(login_url="/login/")
def change_user_groups(request):
    user_id  = request.POST.get('user_id')
    group = request.POST.get('group')
    try:
        user_obj = User.objects.get(id=user_id)
        user_obj.groups.clear()
        user_obj.groups.add(Group.objects.get(name=group))
        user_obj.save()
    except Exception as exc:
        return JsonResponse({'error': f'{exc}'}, status=500)
    return JsonResponse({'response': 'success'}, status=200)


@login_required(login_url="/login/")
def delete_user(request):
    try:
        User.objects.get(id=request.POST.get('user_id')).delete()
    except Exception as exc:
        return JsonResponse({'error': f'{exc}'}, status=500)
    return JsonResponse({'response': 'success'}, status=200)


@login_required(login_url="/login/")
def logs(request):
    if not module_access(request, 'Users'):
        return redirect('/')
    if not request.user.groups.first().access_level >= Module.objects.get(name='Users').access_level:
        return redirect('/')
    context = {}
    return render(request, 'users/logs.html', context=context)


@login_required(login_url="/login/")
def profile(request):
    if request.method == "POST":
        msg = None
        user = User.objects.get(id = request.user.id)
        if len(request.FILES) != 0:
            user.profile_image = request.FILES['profile_image']
        raw_password = request.POST.get("password1")
        # if len(raw_password) != 0:
        #     if raw_password != request.POST.get("password2"):
        #         msg = 'Пароли не совпадают'
        #     elif len(raw_password) < 6:
        #         msg = 'Пароль должен быть больше 6 символов'
        #     else:
        #         msg = 'Пароль изменен'
        #         password = make_password(raw_password, hasher='default')
                # print(password)
                # user.set_password = password
                # user.save()
            # return render(request, 'users/profile.html', {'user_obj': user, 'msg': msg})
        # user.password = raw_password
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.save()

        return redirect('/profile/')
    else:
        form = EditProfileForm(instance=request.user)

        user = request.user
        groups = Group.objects.all().order_by('-access_level')

        context = {
            'groups': groups,
            'user_obj': user,
            'form': form,
        }
        return render(request, 'users/profile.html', context=context)


@login_required(login_url="/login/")
def user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if not user_id == request.user.id and not module_access(request, 'Users'):
        return redirect('/')
    if request.method == "POST":
        user_obj = get_object_or_404(User, id=user_id)
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

