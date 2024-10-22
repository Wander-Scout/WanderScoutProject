from django.urls import path
from . import views

urlpatterns = [
    path('readcsv/', views.readcsv, name='readcsv'),
    path('tourist-attractions/', views.display_attractions_as_cards, name='tourist_attractions'),
]
