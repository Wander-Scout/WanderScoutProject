from django.urls import path
from . import views

app_name = 'authentication'  

urlpatterns = [
    path('login/', views.display_login_form, name='login'),
    path('login/submit/', views.submit_login_form, name='submit_login_form'),
]