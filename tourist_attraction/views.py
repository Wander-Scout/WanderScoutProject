from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import TouristAttraction
from authentication.decorators import admin_only
import json
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse

@require_http_methods(['GET'])
# get the data from the database and return it as a JSON response
def get_tourist_attractions(request):
    attractions = TouristAttraction.objects.all()
    return JsonResponse({'attractions': list(attractions.values())})

@require_http_methods(['GET'])
# display_attractions_as_cards to render the data as cards
def display_attractions_as_cards(request):
    return render(request, 'attraction_cards.html')

@require_http_methods(['GET'])
def attraction_detail(request, attraction_id):
    # Fetch attraction based on UUID and display it in the detail page
    attraction = get_object_or_404(TouristAttraction, id=attraction_id)
    context = {
        'attraction': attraction
    }
    return render(request, 'attraction_detail.html', context)

@admin_only
@login_required
@require_http_methods(['POST'])
def add_tourist_attraction(request):
    # Add attraction based on provided input from the admin empty fields will be defaulted in the html
    try:
        data = json.loads(request.body)
        
        rating = float(data.get('rating', 0.0) or 0.0)
        vote_average = float(data.get('vote_average', 0.0) or 0.0)
        vote_count = int(data.get('vote_count', 0) or 0)
        htm_weekday = float(data.get('htm_weekday', 0.0) or 0.0)
        htm_weekend = float(data.get('htm_weekend', 0.0) or 0.0)
        latitude = float(data.get('latitude', 0.0) or 0.0)
        longitude = float(data.get('longitude', 0.0) or 0.0)
        
        attraction = TouristAttraction.objects.create(
            nama=data.get('nama', 'Unknown Attraction'),
            rating=rating,
            vote_average=vote_average,
            vote_count=vote_count,
            type=data.get('type', 'General'),
            htm_weekday=htm_weekday,
            htm_weekend=htm_weekend,
            description=data.get('description', 'No description available.'),
            gmaps_url=data.get('gmaps_url', 'https://www.google.com/maps'),
            latitude=latitude,
            longitude=longitude,
        )
        return JsonResponse({'message': 'Attraction added successfully.', 'attraction_id': str(attraction.id)}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@admin_only
@login_required
@require_http_methods(['POST'])
def edit_tourist_attraction(request, attraction_id):
    try:
        attraction = get_object_or_404(TouristAttraction, id=attraction_id)
        data = json.loads(request.body)
        
        # Update fields with provided data or keep existing values
        attraction.nama = data.get('nama', attraction.nama)
        attraction.rating = float(data.get('rating', attraction.rating) or attraction.rating)
        attraction.vote_average = float(data.get('vote_average', attraction.vote_average) or attraction.vote_average)
        attraction.vote_count = int(data.get('vote_count', attraction.vote_count) or attraction.vote_count)
        attraction.type = data.get('type', attraction.type)
        attraction.htm_weekday = float(data.get('htm_weekday', attraction.htm_weekday) or attraction.htm_weekday)
        attraction.htm_weekend = float(data.get('htm_weekend', attraction.htm_weekend) or attraction.htm_weekend)
        attraction.description = data.get('description', attraction.description)
        attraction.gmaps_url = data.get('gmaps_url', attraction.gmaps_url)
        attraction.latitude = float(data.get('latitude', attraction.latitude) or attraction.latitude)
        attraction.longitude = float(data.get('longitude', attraction.longitude) or attraction.longitude)
        
        attraction.save()
        return JsonResponse({'message': 'Attraction updated successfully.', 'attraction_id': str(attraction.id)}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@admin_only
@login_required
@require_http_methods(['DELETE'])
def delete_tourist_attraction(request, attraction_id):
    # Delete attraction based on UUID but search if it exist first
    try:
        attraction = get_object_or_404(TouristAttraction, id=attraction_id)
        attraction.delete()
        return JsonResponse({'message': 'Attraction deleted successfully.'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

#------------------------------------------------------------#
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import TouristAttraction
from .serializers import TouristAttractionSerializer

from django.http import JsonResponse

def cors_preflight_handler(request):
    if request.method == "OPTIONS":
        response = JsonResponse({"detail": "Preflight success"})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        return response
    return None

@api_view(['GET', 'OPTIONS'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_tourist_attractions(request):
    origin = request.headers.get('Origin')  # Get the Origin header from the request

    # Handle preflight (OPTIONS) request
    if request.method == 'OPTIONS':
        response = JsonResponse({'detail': 'Preflight request successful'})
        response['Access-Control-Allow-Origin'] = origin  # Dynamically set to the request's Origin
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response

    # Handle GET request
    attractions = TouristAttraction.objects.all()
    serializer = TouristAttractionSerializer(attractions, many=True)

    # Include CORS headers in the GET response
    response = Response(serializer.data)
    response['Access-Control-Allow-Origin'] = origin  # Dynamically set to the request's Origin
    response['Access-Control-Allow-Credentials'] = 'true'
    return response
