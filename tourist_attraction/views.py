import pandas as pd
import os
from django.http import JsonResponse
from django.conf import settings
from .models import TouristAttraction
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

@require_http_methods(["GET"])
def readcsv(request):
    # Build the path to the CSV file in the static/data directory in the root
    static_dir = os.path.join(settings.BASE_DIR, 'static', 'data')
    csv_file_path = os.path.join(static_dir, 'TempatWisata.csv')

    if not os.path.exists(csv_file_path):
        return JsonResponse({'error': 'CSV file not found'}, status=404)

    # Read CSV using pandas
    df = pd.read_csv(csv_file_path)

    # List to store the created objects
    attractions = []

    # Iterate over the rows in the DataFrame
    for _, row in df.iterrows():
        attraction = TouristAttraction.objects.create(
            name=row['nama'],
            rating=row['vote_average'],
            attraction_type=row['type'],  # Renamed field
            htmweekday=row['htm_week'],
            htmweekend=row['htm_weekend'],  # Corrected typo here
            description=row['description'],
            gmapsurl=row['gmaps_url']
        )
        attractions.append({
            'id': str(attraction.id),
            'name': attraction.name,
            'rating': float(attraction.rating),
            'attraction_type': attraction.attraction_type,
            'htmweekday': attraction.htmweekday,
            'htmweekend': attraction.htmweekend,
            'description': attraction.description,
            'gmapsurl': attraction.gmapsurl
        })

    # Return the list of created attractions as a JSON response
    return JsonResponse(attractions, safe=False)

def display_attractions_as_cards(request):
    attractions = TouristAttraction.objects.all()
    return render(request, 'attraction_cards.html', {'attractions': attractions})  # Corrected template name
