from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('neighbourhood/', views.neighborhoods, name='neighbourhood'),
    path('view/<str:name>', views.view_neighbourhood, name='view'),
    path('join/<str:name>', views.join_neighbourhood, name='join'),
    path('selected/<str:name>', views.self_neigbourhood, name='selected'),
    path('create/', views.create_neighbourhood, name='create'),
    path('leave/<str:name>', views.leave_neighbourhood, name='leave'),
    path('updates/<str:name>', views.add_updates, name='updates'),
    path('add_business/<str:name>', views.add_business, name='business'),
    # password recovery
    path('password-reset/', 
    auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'), 
    name='password_reset'),
    path('password-reset/done/', 
    auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), 
    name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', 
    auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'), 
    name='password_reset_confirm'),
     path('password-reset-complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), 
    name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)