from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from restaurant.models import Restaurant
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant
import json
from authentication.decorators import admin_only

@require_http_methods(['GET'])
def get_restaurants(request):
    # Fetch all restaurants from the database
    restaurants = Restaurant.objects.all()
    # Return restaurants as JSON
    return JsonResponse({'restaurants': list(restaurants.values())})

@require_http_methods(['GET'])
def display_restaurants_as_cards(request):
    # Fetch all restaurants from the database
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    # Render the restaurant cards template with restaurant data
    return render(request, 'restaurant_cards.html', context)


@require_http_methods(['GET'])
def restaurant_detail(request, restaurant_id):
    # Fetch restaurant based on UUID
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    context = {
        'restaurant': restaurant
    }
    # Render the restaurant detail template
    return render(request, 'restaurant_detail.html', context)


@require_http_methods(['POST'])
@admin_only  # Restrict this view to admin users
def add_restaurant(request):
    try:
        data = json.loads(request.body)
        restaurant = Restaurant.objects.create(
            name=data['name'],
            food_preference=data['food_preference'],
            average_price=data['average_price'],
            rating=data['rating'],
            atmosphere=data['atmosphere'],
            food_variety=data['food_variety']
        )
        return JsonResponse({'message': 'Restaurant added successfully!', 'restaurant': restaurant.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)