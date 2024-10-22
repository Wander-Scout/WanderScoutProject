from django.db import models

class TouristAttraction(models.Model):
    name = models.CharField(max_length=255)
    rating = models.FloatField()
    attraction_type = models.CharField(max_length=255)
    htmweekday = models.DecimalField(max_digits=10, decimal_places=2)
    htmweekend = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    gmapsurl = models.URLField()
