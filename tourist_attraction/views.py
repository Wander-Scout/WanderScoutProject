from .models import TouristAttraction
import random
from django.http import JsonResponse
from .models import TouristAttraction
from django.views.decorators.http import require_http_methods
from tourist_attraction.models import TouristAttraction
from django.shortcuts import render, get_object_or_404

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
