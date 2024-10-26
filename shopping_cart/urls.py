# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/<uuid:attraction_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<uuid:attraction_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('booking/<uuid:booking_id>/', views.booking_detail_view, name='booking_detail'),
    path('search-booking/', views.search_booking_view, name='search_booking'),
    path('past-bookings/', views.past_bookings_view, name='past_bookings'),
]

