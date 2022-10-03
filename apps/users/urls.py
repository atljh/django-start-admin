from django.urls import path
from apps.users import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('users/', views.users, name='users'),
    path('modules/', views.modules, name='modules'),

    path('modules/change_access/', views.change_module_accces, name='modules-change-access'),
    path('users/change_user_group/', views.change_user_group, name='user-change-group'),
    path('users/delete_user/', views.delete_user, name='delete-user'),

    path('logs/', views.logs, name='logs'),
    path('profile/', views.profile, name='profile'),
    path('user/<int:user_id>/', views.user, name='user'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

