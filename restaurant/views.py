from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from restaurant.models import Restaurant
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant
import json
from authentication.decorators import admin_only
from django.contrib.auth.decorators import login_required
import logging

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
@admin_only
def add_restaurant(request):
    if not request.user.is_staff:  # Check if the user is an admin
        return JsonResponse({'error': 'Admin access required.'}, status=403)

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
        return JsonResponse({'success': True, 'restaurant': restaurant.id})
    except Exception as e:
        print(f"Error adding restaurant: {e}")  # Logs error to the server console
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    

logger = logging.getLogger(__name__)
@require_http_methods(["GET"])
@admin_only
def delete_restaurant(request, restaurant_id):
    if not request.user.is_staff:  # Check if the user is an admin
        return JsonResponse({'error': 'Admin access required.'}, status=403)

    try:
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        restaurant.delete()
        return JsonResponse({"success": True, "message": "Restaurant deleted successfully"})
    except Restaurant.DoesNotExist:
        return JsonResponse({"success": False, "message": "Restaurant not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
    

@login_required
@admin_only
@require_http_methods(["GET"])
def get_restaurant_data(request, restaurant_id):
    """Fetch restaurant data for editing."""
    logger.info(f"Fetching data for restaurant_id: {restaurant_id}")
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return JsonResponse({
        "name": restaurant.name,
        "food_preference": restaurant.food_preference,
        "average_price": restaurant.average_price,
        "rating": restaurant.rating,
        "atmosphere": restaurant.atmosphere,
        "food_variety": restaurant.food_variety,
    })

@login_required
@require_http_methods(["POST"])
@admin_only
def update_restaurant(request, restaurant_id):
    """Update restaurant details."""
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    try:
        data = json.loads(request.body)
        restaurant.name = data.get("name", restaurant.name)
        restaurant.food_preference = data.get("food_preference", restaurant.food_preference)
        restaurant.average_price = data.get("average_price", restaurant.average_price)
        restaurant.rating = data.get("rating", restaurant.rating)
        restaurant.atmosphere = data.get("atmosphere", restaurant.atmosphere)
        restaurant.food_variety = data.get("food_variety", restaurant.food_variety)
        restaurant.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)