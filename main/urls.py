from django.urls import path
from . import views
from main.views import login_user


urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home_page, name='home_page'),
]