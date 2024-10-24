from django.db import migrations
import os
from django.core.management import call_command
from django.conf import settings

def load_my_initial_data(apps, schema_editor):
    # Construct the full path to the JSON file in the static/data folder
    json_file_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'TempatWisata.json')
    
    # Call loaddata with the full path
    call_command("loaddata", json_file_path)

class Migration(migrations.Migration):

    dependencies = [
        ('tourist_attraction', '0004_rename_gmapsurl_touristattraction_gmaps_url_and_more'),
    ]

    operations = [
        migrations.RunPython(load_my_initial_data),
    ]