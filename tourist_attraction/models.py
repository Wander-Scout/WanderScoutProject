import uuid
from django.db import models

#Based off the original csv file
class TouristAttraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    no = models.IntegerField(default=0)
    nama = models.CharField(max_length=255, default='Unknown Attraction')
    rating = models.FloatField(default=0.0)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)
    type = models.CharField(max_length=255, default='General')
    htm_weekday = models.FloatField(default=0.0)
    htm_weekend = models.FloatField(default=0.0)
    description = models.TextField(default='No description available.')
    gmaps_url = models.URLField(default='https://www.google.com/maps')
    latitude = models.FloatField(null=True, blank=True, default=0.0)
    longitude = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return self.name
