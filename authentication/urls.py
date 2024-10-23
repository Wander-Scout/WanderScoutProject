from django.urls import path
from . import views

app_name = 'authentication'  

urlpatterns = [
    path('login/', views.display_login_form, name='login'),
    path('login/submit/', views.submit_login_form, name='submit_login_form'),
    path('register/', views.display_register_form, name='display_register_form'),
    path('register/submit/', views.submit_register_form, name='submit_register_form'),
]