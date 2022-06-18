from . import views
from django.urls import path


urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('update-profile/', views.update_profile, name='update-profile'),

    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('neigbourhood/', views.hoods, name='hoods'),
    path('join/<str:name>', views.join_hood, name='join-hood'),
    path('hoods/<str:name>', views.single_hood, name='hood'),
    path('create-hood/', views.create_hood, name='create-hood')
]