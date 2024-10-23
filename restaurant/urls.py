from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.display_restaurants_as_cards, name='restaurants'),
    path('import-restaurants/', views.import_json_to_db, name='import_restaurants'),
]
