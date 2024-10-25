from django.urls import path
from . import views

urlpatterns = [
    path('add/<uuid:attraction_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<uuid:attraction_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('', views.view_cart, name='view_cart'),
]
