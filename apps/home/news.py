import os, environ
from core.settings import BASE_DIR
import finnhub
from .models import News, ReferenceNews
from datetime import datetime, timedelta
import csv  

env = environ.Env(
    DEBUG=(bool, True))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

finnhub_client = finnhub.Client(api_key=env('FINNHUB'))


def get_references():
    with open("EtalonNews.tsv") as f:
        for line in f:
            id = line.split()[0]
            globalreport = ' '.join(line.split()[1:])
            ReferenceNews.objects.create(news_id=int(id), globalreport=globalreport)


def get_new_news():
    result = finnhub_client.calendar_economic().get('economicCalendar')
    return result


def get_news(date_from: str, date_to: str):
    try:
        result = finnhub_client.calendar_economic(date_from, date_to).get('economicCalendar')
    except Exception as exc:
        print(exc) 
        return []
    return result


def save_news(date_from: str, date_to: str):
    news = get_news(date_from, date_to)
    for new in news:
        new['date'] = new['time'][:10]
        new['time'] = new['time'][11:]
    if len(news) >= 2000:
        save_news(news[-1]['date'], date_to)
    News.objects.bulk_create([News(**new) for new in news], ignore_conflicts=True)



def update_news(date_from, date_to):
    News.objects.filter(date__range=[date_from, date_to]).delete()
    save_news(date_from, date_to)
    news = News.objects.filter(date__range=[date_from, date_to])
    if len(news) >= 2000:
        news = News.objects.filter(date__range=[date_from, date_to])[:2000]


    return news


def save_task():
    date_to = datetime.strftime(datetime.now(), '%Y-%m-%d')
    current_date = datetime.strptime('2008-03-22', '%Y-%m-%d')