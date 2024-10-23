import os
import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import TouristAttraction
from django.views.decorators.http import require_http_methods

import os
import json
from django.http import JsonResponse
from django.conf import settings
from .models import TouristAttraction
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def import_json_to_db(request):
    # Path to the JSON file (modify this to your file's location)
    json_file_path = os.path.join(settings.BASE_DIR, 'static', 'TempatWisata.json')

    # Check if the file exists
    if not os.path.exists(json_file_path):
        return JsonResponse({'error': 'JSON file not found'}, status=404)

    # Load and read the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': f'Error reading JSON file: {str(e)}'}, status=400)

    # Iterate through the data and create TouristAttraction objects
    for item in data:
        try:
            # Create a new TouristAttraction object
            TouristAttraction.objects.create(
                name=item.get('name', 'Unknown'),
                rating=item.get('rating', 0.0),
                vote_count=item.get('vote_count', 0),
                attraction_type=item.get('type', 'Unknown'),
                htmweekday=item.get('htm_weekday', 0.0),
                htmweekend=item.get('htm_weekend', 0.0),
                description=item.get('description', ''),
                gmapsurl=item.get('gmaps_url', ''),
                latitude=item.get('latitude', 0.0),
                longitude=item.get('longitude', 0.0)
            )
        except KeyError as ke:
            return JsonResponse({'error': f'Missing key in JSON: {str(ke)}'}, status=400)
        except ValueError as ve:
            return JsonResponse({'error': f'Invalid value in JSON: {str(ve)}'}, status=400)

    return JsonResponse({'message': 'Tourist attractions imported successfully.'})

@require_http_methods(['GET'])
def display_attractions_as_cards(request):
    return render(request, 'attraction_cards.html')

