from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('update-profile/', views.update_profile, name='update-profile'),
    # path('contact/', views.contact, name='contact'),
    # path('about/', views.about, name='about'),
    path('neigbourhood/', views.neighborhoods, name='neigbourhood'),
    path('new/<str:name>', views.new_neighborhood, name='new'),
    path('hoods/<str:name>', views.self_neigbourhood, name='hood'),
    path('create/', views.create_neighbourhood, name='create')
]