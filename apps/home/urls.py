from django.urls import path
from apps.home import views

urlpatterns = [

    path('', views.dashboard, name='home'),

    path('calendar/', views.calendar, name='calendar'),
    path('calendar/get_news/', views.get_selected_news, name='get-selected-news'),
    path('calendar/search_date/', views.search_date, name='search-date'),
    path('calendar/select_news/', views.select_news, name='select-news'),
    path('calendar/set_timezone/', views.set_timezone, name='set-timezone'),

    path('charts/', views.charts, name='charts'),
]
