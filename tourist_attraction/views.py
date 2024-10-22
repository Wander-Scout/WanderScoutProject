import pandas as pd
import os
from django.http import JsonResponse
from django.conf import settings
from .models import TouristAttraction
from django.views.decorators.http import require_http_methods



@require_http_methods(["GET"])
def upload_csv_from_static_and_return_json(request):
    if request.method == "GET":
        # Build the path to the CSV file in the static/csv directory
        csv_file_path = os.path.join(settings.BASE_DIR, 'static', 'csv', 'yourfile.csv')

        # Read CSV with pandas
        df = pd.read_csv(csv_file_path)

        # List to store the created objects
        attractions = []

        # Iterate over the rows in the DataFrame
        for _, row in df.iterrows():
            attraction = TouristAttraction.objects.create(
                name=row['nama'],
                rating=row['vote_average'],
                type=row['type'],
                htmweekday=row['htm_week'],
                htmweekend=row['htm_weel'],
                description=row['description'],
                gmapsurl=row['gmaps_url']
            )
            attractions.append({
                'id': str(attraction.id),
                'name': attraction.name,
                'rating': float(attraction.rating),
                'type': attraction.type,
                'htmweekday': attraction.htmweekday,
                'htmweekend': attraction.htmweekend,
                'description': attraction.description,
                'gmapsurl': attraction.gmapsurl
            })
        return JsonResponse(attractions, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)
