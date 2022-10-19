import os, environ
from core.settings import BASE_DIR
import finnhub
from .models import News, ReferenceNews, AuctionTools
from datetime import datetime, timedelta


env = environ.Env(
    DEBUG=(bool, True))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

finnhub_client = finnhub.Client(api_key=env('FINNHUB'))


def get_references():
    with open("EtalonNews.tsv") as file:
        for line in file:
            id = line.split()[0]
            globalreport = ' '.join(line.split()[1:])
            ReferenceNews.objects.create(news_id=int(id), globalreport=globalreport)


def get_auction_tools():
    with open("AuctionTools.tsv") as file:
        for line in file:
            name = line.split()[0]
            description = ' '.join(line.split()[1:-1])
            symbol = line.split()[-1]
            AuctionTools.objects.create(name=name, description=description, symbol=symbol)


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
        last_date = news[-1]['date']
        News.objects.bulk_create([News(**new) for new in news if new['date'] != last_date], ignore_conflicts=True)
        save_news(last_date, date_to)
    else:
        News.objects.bulk_create([News(**new) for new in news], ignore_conflicts=True)



def update_news(date_from: str, date_to: str):
    News.objects.filter(date__range=[date_from, date_to]).delete()
    save_news(date_from, date_to)
    news = News.objects.filter(date__range=[date_from, date_to])
    
    if len(news) >= 2000:
        news = News.objects.filter(date__range=[date_from, date_to])[:2000]
    return news
