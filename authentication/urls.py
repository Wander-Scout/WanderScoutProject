from django.urls import path
from . import views

app_name = 'authentication'  

urlpatterns = [
    path('login/', views.display_login_form, name='login'),
    path('login/submit/', views.submit_login_form, name='submit_login_form'),
    path('register/', views.display_register_form, name='display_register_form'),
    path('register/submit/', views.submit_register_form, name='submit_register_form'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.display_edit_profile_page, name='profile'),
    path('profile-data/', views.display_edit_profile, name='display_edit_profile'),
    path('profile-submit/', views.submit_edit_profile, name='submit_edit_profile'),
]