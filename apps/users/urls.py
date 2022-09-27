from django.urls import path, re_path
from apps.users import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('users-observe/', views.users_observe, name='users-observe'),
    path('users-control/', views.users_control, name='users-control'),
    path('logs/', views.logs, name='logs'),
    path('profile/', views.profile, name='profile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

