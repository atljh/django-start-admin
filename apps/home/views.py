from datetime import date, datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Module
from .news import update_news, get_references
from .models import News, ReferenceNews
from django.core import serializers
from itertools import chain
from apps.users.models import User

def module_access(request, module: str) -> bool:
    if request.user.groups.first().access_level >= Module.objects.get(name=module).access_level:
        return True
    return False


def get_module(request):
    module = request.GET.get('module')
    if request.user.groups.first().access_level >= Module.objects.get(name=module).access_level:
        return JsonResponse({'ok': f'{module}'})
    else:
        return JsonResponse({'error': f'{module}'})


@login_required(login_url="/login/")
def dashboard(request):
    if not module_access(request, 'Dashboard'):
        return redirect('/login/')
    return render(request, 'home/dashboard.html')



@login_required(login_url="/login/")
def calendar(request):
    if not module_access(request, 'Calendar'):
        return redirect('/login/')

    if request.GET.get('search_date'):
        data = search_date(request.GET.get('search_date'))
        return JsonResponse(data, safe=False, status=200)

    if request.GET.get('news_id'):
        data = get_news_by_id(request.GET.get('news_id'))
        return JsonResponse(data, safe=False, status=200)

    if request.GET.get('news'):
        news_id = int(request.GET.get('news'))
        new = News.objects.get(pk=news_id)
        news = News.objects.filter(event=new.event)
        return render(request, 'modules/calendar.html', {'news': news})

    if request.GET.get('timezone'):
        set_timezone(request.user.id, request.GET.get('timezone'))
        return JsonResponse({'timezone': request.user.timezone}, status=200)

    if request.GET.get('date_from'):
        data = search_range(request.GET.get('date_from'), request.GET.get('date_to'))
        return JsonResponse(data, safe=False, status=200)

    if request.GET.get('select_news'):
        data = select_news(request.GET.get('select_news'))
        return JsonResponse(data, safe=False, status=200)


    news = News.objects.filter(date=date.today())

    context = {
        'news': news,
        'timezone': request.user.timezone,
    }
    
    return render(request, 'modules/calendar.html', context=context)


def select_news(select_news):
    if select_news == 'Economic releases':
        news = News.objects.filter(date=date.today())

    elif select_news == 'Etalon news':
        news = ReferenceNews.objects.all()
        if len(news) < 1:
            get_references()
            news = ReferenceNews.objects.all()

    data = serializers.serialize('json', news)
    return data


def get_news_by_id(news_id):
    try:
        new = News.objects.get(pk=news_id)
    except Exception as exc:
        print(exc)
        news = []
    else:
        news_same_time = News.objects.filter(date=new.date, time=new.time)
        news_same_event = News.objects.filter(event=new.event).exclude(pk=new.pk).order_by('-date')
        news = list(chain(news_same_time, news_same_event))

    data = serializers.serialize('json', news)
    return data


def search_date(search_value):

    if search_value == 'today':
        today = date.today()
        news = update_news(today, today)

    elif search_value == 'tomorrow':
        tomorrow = date.today()+timedelta(days=1)
        news = update_news(tomorrow, tomorrow)

    elif search_value == 'this week':
        now = datetime.now()
        monday = now - timedelta(days = now.weekday())
        sunday = monday + timedelta(days=6)
        monday = monday.strftime('%Y-%m-%d')
        sunday = sunday.strftime('%Y-%m-%d')
        news = update_news(monday, sunday)

    elif search_value == 'next week':
        now = datetime.now()
        monday = now - timedelta(days = now.weekday()) + timedelta(days=7)
        sunday = monday + timedelta(days=6) + timedelta(days=7)
        monday = monday.strftime('%Y-%m-%d')
        sunday = sunday.strftime('%Y-%m-%d')
        news = update_news(monday, sunday)

    data = serializers.serialize('json', news)
    return data


def search_range(date_from, date_to):
    news = update_news(date_from, date_to)
    data = serializers.serialize('json', news)
    return data


def set_timezone(user_id, timezone):
    user = User.objects.get(pk=user_id)
    user.timezone = timezone
    user.save()


