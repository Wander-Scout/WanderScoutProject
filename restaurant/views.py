import os
import json
from django.http import JsonResponse
from django.conf import settings
from .models import Restaurant
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

@require_http_methods(["POST"])
def import_json_to_db(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'Kuliner.json')

    if not os.path.exists(json_file_path):
        return JsonResponse({'error': 'JSON file not found'}, status=404)

    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': f'Error reading JSON file: {str(e)}'}, status=400)

    for item in data:
        try:
            Restaurant.objects.create(
                name=item.get('Nama Restoran', 'Unknown'),
                food_preference=item.get('Preferensi Makanan', 'Unknown'),
                average_price=item.get('Harga Rata-Rata Makanan di Toko (Rp)', 0),
                rating=item.get('Rating Toko', 0.0),
                atmosphere=item.get('Jenis Suasana', 'Unknown'),
                food_variety=item.get('Variasi Makanan', 'Unknown')
            )
        except KeyError as ke:
            return JsonResponse({'error': f'Missing key in JSON: {str(ke)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error saving data: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Restaurants imported successfully.'})

@require_http_methods(['GET'])
def display_restaurants_as_cards(request):
    return render(request, 'restaurant_cards.html')
