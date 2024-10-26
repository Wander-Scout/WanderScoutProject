from django.urls import path
from . import views

app_name = 'authentication'  

urlpatterns = [
    path('login/', views.display_login_form, name='login'),
    path('login/submit/', views.submit_login_form, name='submit_login_form'),
    path('register/', views.display_register_form, name='display_register_form'),
    path('register/submit/', views.submit_register_form, name='submit_register_form'),
    path('logout/', views.logout_user, name='logout_user'),
    path('edit-profile/', views.display_edit_profile_page, name='edit_profile_page'),  # New view for the HTML page
    path('edit-profile-data/', views.display_edit_profile, name='display_edit_profile'),  # JSON data for AJAX
    path('submit-edit-profile/', views.submit_edit_profile, name='submit_edit_profile'),
    path('profile/', views.profile_view, name='profile'),
]