from django.urls import path
from apps.home import charts, views

urlpatterns = [

    path('', views.dashboard, name='home'),

    path('get_module/', views.get_module, name='get-module'),
    path('calendar/', views.calendar, name='calendar'),
    
    path('charts/', charts.charts, name='charts'),
    path('charts/<news_id>/', charts.charts, name='charts'),

]
