from django.urls import path
from . import views

urlpatterns = [
    path('tourist-attractions/', views.display_attractions_as_cards, name='tourist_attractions'),
    path('api/', views.get_tourist_attractions, name='get_tourist_attractions'),
    path('attractions/<uuid:attraction_id>/', views.attraction_detail, name='attraction_detail'),
    path('add_attraction/', views.add_tourist_attraction, name='add_tourist_attraction'),
    path('delete_attraction/<uuid:attraction_id>/', views.delete_tourist_attraction, name='delete_tourist_attraction'),
    path('edit_attraction/<uuid:attraction_id>/', views.edit_tourist_attraction, name='edit_tourist_attraction'),
    path('api_tourist_attractions', views.api_tourist_attractions, name='api_tourist_attractions'),
    path('api_tourist_attractions/add', views.add_tourist_attraction_flutter, name='add_tourist_attraction'),
    path('api_tourist_attractions/edit/<uuid:attraction_id>/', views.edit_tourist_attraction_flutter, name='edit_tourist_attraction'),
    path('api_tourist_attractions/delete/<uuid:attraction_id>/', views.delete_tourist_attraction_flutter, name='delete_tourist_attraction'),
]
