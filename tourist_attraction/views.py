from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import TouristAttraction
from authentication.decorators import admin_only
import json

@require_http_methods(['GET'])
def get_tourist_attractions(request):
    attractions = TouristAttraction.objects.all()
    return JsonResponse({'attractions': list(attractions.values())})

@require_http_methods(['GET'])
def display_attractions_as_cards(request):
    return render(request, 'attraction_cards.html')

@require_http_methods(['GET'])
def attraction_detail(request, attraction_id):
    # Fetch attraction based on UUID
    attraction = get_object_or_404(TouristAttraction, id=attraction_id)
    context = {
        'attraction': attraction
    }
    return render(request, 'attraction_detail.html', context)

@admin_only
@require_http_methods(['POST'])
def add_tourist_attraction(request):
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
        # Log the exception details for debugging
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=400)

@admin_only
@require_http_methods(['DELETE'])
def delete_tourist_attraction(request, attraction_id):
    try:
        attraction = get_object_or_404(TouristAttraction, id=attraction_id)
        attraction.delete()
        return JsonResponse({'message': 'Attraction deleted successfully.'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
