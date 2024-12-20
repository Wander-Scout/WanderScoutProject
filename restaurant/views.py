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
from django.core import serializers
from django.http import HttpResponse

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

    try: # parse the JSON data in request body
        data = json.loads(request.body)
        restaurant = Restaurant.objects.create( # create a new restaurant entry in the database
            name=data['name'],
            food_preference=data['food_preference'],
            average_price=data['average_price'],
            rating=data['rating'],
            atmosphere=data['atmosphere'],
            food_variety=data['food_variety']
        ) # return success message with the new restaurant's ID
        return JsonResponse({'success': True, 'restaurant': restaurant.id})
    except Exception as e: # log error on server
        print(f"Error adding restaurant: {e}")  # Logs error to the server console
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    

logger = logging.getLogger(__name__)
@require_http_methods(["GET"])
@admin_only
def delete_restaurant(request, restaurant_id):
    if not request.user.is_staff:  # Check if the user is an admin
        return JsonResponse({'error': 'Admin access required.'}, status=403)

    try: # get the restaurant by primary key (or 404 if not found)
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        restaurant.delete() # delete the restaurant
        return JsonResponse({"success": True, "message": "Restaurant deleted successfully"})
    except Restaurant.DoesNotExist: # return a not found message if restaurant doesn’t exist
        return JsonResponse({"success": False, "message": "Restaurant not found"}, status=404)
    except Exception as e: # handle other errors
        return JsonResponse({"success": False, "message": str(e)}, status=500)
    

@login_required
@admin_only
@require_http_methods(["GET"])
def get_restaurant_data(request, restaurant_id):
    """Fetch restaurant data for editing."""
    logger.info(f"Fetching data for restaurant_id: {restaurant_id}") 
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)  # get restaurant by ID or return 404 if not found
    return JsonResponse({  # return restaurant data as JSON
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
    """Update restaurant details."""  # fetch restaurant by ID or return 404
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    try: # parse JSON data in request body
        data = json.loads(request.body)  # update restaurant attributes if provided
        restaurant.name = data.get("name", restaurant.name) 
        restaurant.food_preference = data.get("food_preference", restaurant.food_preference)
        restaurant.average_price = data.get("average_price", restaurant.average_price)
        restaurant.rating = data.get("rating", restaurant.rating)
        restaurant.atmosphere = data.get("atmosphere", restaurant.atmosphere)
        restaurant.food_variety = data.get("food_variety", restaurant.food_variety)  # save changes to the database
        restaurant.save() 
        return JsonResponse({"success": True}) # return success message
    except Exception as e: # return error message if an exception occurs
        return JsonResponse({"success": False, "error": str(e)}, status=400)
    
#------------------------------------------------------------#
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Restaurant
from .serializers import RestaurantSerializer

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_restaurant(request):
    attractions = Restaurant.objects.all()
    serializer = RestaurantSerializer(attractions, many=True)
    return Response(serializer.data)


# restaurant/views.py

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from authentication.decorators import admin_only
from django.http import JsonResponse
from .models import Restaurant

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_only
def add_restaurant(request):
    data = request.data
    name = data.get('name')
    food_preference = data.get('food_preference')
    average_price = data.get('average_price')
    rating = data.get('rating')
    atmosphere = data.get('atmosphere')
    food_variety = data.get('food_variety')

    # Validate data
    if not all([name, food_preference, average_price, rating, atmosphere, food_variety]):
        return JsonResponse({'status': False, 'message': 'All fields are required.'}, status=400)

    try:
        average_price = int(average_price)
        rating = float(rating)
    except ValueError:
        return JsonResponse({'status': False, 'message': 'Invalid data type for price or rating.'}, status=400)

    # Create the restaurant
    restaurant = Restaurant.objects.create(
        name=name,
        food_preference=food_preference,
        average_price=average_price,
        rating=rating,
        atmosphere=atmosphere,
        food_variety=food_variety,
    )
    return JsonResponse({'status': True, 'message': 'Restaurant added successfully.'}, status=201)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Restaurant

@csrf_exempt
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_only
def delete_restaurant(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)  # UUID or int
        restaurant.delete()
        return JsonResponse({'status': True, 'message': 'Restaurant deleted successfully.'}, status=200)
    except ValueError:
        return JsonResponse({'status': False, 'message': 'Invalid ID format.'}, status=400)
    except Restaurant.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Restaurant not found.'}, status=404)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Restaurant
from authentication.decorators import admin_only
import json

@csrf_exempt
@admin_only
def edit_restaurant(request, restaurant_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            restaurant = get_object_or_404(Restaurant, id=restaurant_id)

            # Update restaurant details
            restaurant.name = data.get("name", restaurant.name)
            restaurant.food_preference = data.get("food_preference", restaurant.food_preference)
            restaurant.average_price = data.get("average_price", restaurant.average_price)
            restaurant.rating = data.get("rating", restaurant.rating)
            restaurant.atmosphere = data.get("atmosphere", restaurant.atmosphere)
            restaurant.food_variety = data.get("food_variety", restaurant.food_variety)

            restaurant.save()

            return JsonResponse({"message": "Restaurant updated successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)

