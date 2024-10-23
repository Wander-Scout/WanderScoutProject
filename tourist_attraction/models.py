from django.db import models

class TouristAttraction(models.Model):
    name = models.CharField(max_length=255, default='Unknown Attraction')
    rating = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)
    attraction_type = models.CharField(max_length=255, default='General')
    htmweekday = models.FloatField(default=0.0)
    htmweekend = models.FloatField(default=0.0)
    description = models.TextField(default='No description available.')
    gmapsurl = models.URLField(default='https://www.google.com/maps')
    latitude = models.FloatField(null=True, blank=True, default=0.0)
    longitude = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return self.name
