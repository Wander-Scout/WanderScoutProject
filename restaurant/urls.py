from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_restaurants_as_cards, name='restaurants'),  # Display restaurant list
    path('api/', views.get_restaurants, name='get_restaurants'),  # API for restaurants
    path('restaurant/<uuid:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),  # Restaurant detail
    path('api/add_restaurant/', views.add_restaurant, name='add_restaurant'),
    path('api/delete_restaurant/<uuid:restaurant_id>/', views.delete_restaurant, name='delete_restaurant'),
    
]
