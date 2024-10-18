from django.urls import path
from . import views

urlpatterns = [
    path('get-all-restaurants/', views.get_all_restaurants, name='get_all_restaurants'),
]
