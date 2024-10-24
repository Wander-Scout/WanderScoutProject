from django.urls import path
from . import views

urlpatterns = [
    path('tourist-attractions/', views.display_attractions_as_cards, name='tourist_attractions'),
    path('api/', views.get_tourist_attractions, name='get_tourist_attractions'),
    path('attractions/<uuid:attraction_id>/', views.attraction_detail, name='attraction_detail')

]
