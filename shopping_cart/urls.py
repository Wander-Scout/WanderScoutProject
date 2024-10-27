from django.urls import path
from . import views

urlpatterns = [
    # Adds an item to the cart based on the item’s unique ID. Think of it as "grabbing" an attraction or restaurant to your list.
    path('add/<uuid:item_id>/', views.add_to_cart, name='add_to_cart'),
    
    # Removes an item from the cart by its unique ID. Use this when you’ve decided to skip an attraction or dining spot.
    path('remove/<uuid:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Shows the cart view where you can see everything you’ve added so far.
    path('', views.view_cart, name='view_cart'),
    
    # Initiates the checkout process when you’re ready to finalize your selections.
    path('checkout/', views.checkout_view, name='checkout'),
    
    # Allows you to search for a specific booking by its ID, useful when you need quick access to a specific booking.
    path('search-booking/', views.search_booking_view, name='search_booking'),
    
]
