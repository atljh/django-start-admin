from django.urls import path
from apps.home import views

urlpatterns = [

    path('', views.dashboard, name='home'),

    path('calendar/', views.calendar, name='calendar'),
    path('charts/', views.charts, name='charts'),
]
