from datetime import date, datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Module
from .news import get_news, save_news, save_task, get_new_news, update_news, get_references
from .models import News, ReferenceNews
from django.core import serializers
from itertools import chain
from apps.users.models import User

def module_access(request, module: str) -> bool:
    if request.user.groups.first().access_level >= Module.objects.get(name=module).access_level:
        return True
    return False


@login_required(login_url="/login/")
def dashboard(request):
    if not module_access(request, 'Dashboard'):
        return redirect('/login/')
    return render(request, 'home/dashboard.html')



@login_required(login_url="/login/")
def calendar(request):
    if not module_access(request, 'Calendar'):
        return redirect('/login/')

    news = News.objects.filter(date=date.today())
    # news = News.objects.all()
    context = {
        'news': news,
        'timezone': request.session.get('timezone'),
    }
    
    return render(request, 'modules/calendar.html', context=context)


def select_news(request):
    select_news = request.GET.get('news')
    if select_news == 'Economic releases':
        news = News.objects.filter(date=date.today())
    elif select_news == 'Etalon news':
        news = ReferenceNews.objects.all()[:10]

    data = serializers.serialize('json', news)
    return JsonResponse(data, safe=False, status=200)


def get_selected_news(request):
    news_id = request.GET.get('news_id')
    try:
        new = News.objects.get(pk=news_id)
    except Exception:
        news = []
    else:
        news_same_time = News.objects.filter(date=new.date, time=new.time)
        news_same_event = News.objects.filter(event=new.event).exclude(pk=new.pk).order_by('-date')
        news = list(chain(news_same_time, news_same_event))
    data = serializers.serialize('json', news)
    return JsonResponse(data, safe=False, status=200)


def search_date(request):
    search_value = request.GET.get('search_date')
    news = []

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

    elif request.GET.get('date_from'):
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        news = update_news(date_from, date_to)

    data = serializers.serialize('json', news)
    return JsonResponse(data, safe=False, status=200)


def set_timezone(request):
    timezone = request.GET.get('timezone')
    user = User.objects.get(pk=request.user.pk)
    user.timezone = timezone
    user.save()
    return JsonResponse({'response': 'ok'}, status=200)


@login_required(login_url="/login/")
def charts(request):
    if not module_access(request, 'Charts'):
        return redirect('/login/')
    context = {}
    return render(request, 'modules/charts.html', context=context)



# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))
