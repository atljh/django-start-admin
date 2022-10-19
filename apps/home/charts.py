from .metatrader import mass_import
from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import News,  AuctionTools
from django.shortcuts import get_object_or_404
from .news import get_auction_tools
from django.core import serializers
from .views import module_access



@login_required(login_url="/login/")
def charts(request, news_id=None):
    if not module_access(request, 'Charts'):
        return redirect('/login/')
    
    if request.GET.get('get_tools'):
        tools = AuctionTools.objects.all()
        if len(tools) < 1:
            get_auction_tools()
            tools = AuctionTools.objects.all()

        data = serializers.serialize('json', tools)
        return JsonResponse({'tools': data}, safe=False, status=200)

    if request.GET.get('get_chart'):
        horizon = request.GET.get('horizon')
        asset_name = request.GET.get('get_chart', 'M1')
        if request.GET.get('date'):
            date = datetime.strptime(request.GET.get('date'), "%d.%m.%Y %H:%M")
        else:
            date = datetime.now()
        asset = AuctionTools.objects.get(name=asset_name).symbol
        ticks = mass_import(asset, horizon, date.year, date.month, date.day, date.hour, date.minute)

        return JsonResponse(ticks, safe=False)

    if not news_id: 
        return render(request, 'modules/charts.html')


    news = get_object_or_404(News, pk=news_id)

    prev = News.objects.filter(event=news.event, date__lt=news.date).order_by('-date').values('date', 'pk')[:1]
    next = News.objects.filter(event=news.event, date__gt=news.date).order_by('date').values('date', 'pk')[:1]
    
    try:
        prev = prev[0]
    except IndexError:
        prev = []
    try:
        next = next[0]
    except IndexError:
        next = []

    context = {
        'news': news,
        'prev': prev,
        'next': next,
    }

    return render(request, 'modules/charts.html', context=context)
