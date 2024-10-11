from django.db import models
import uuid

class TouristAttraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    type = models.CharField(max_length=100)
    htmweekday = models.IntegerField()
    htmweekend = models.IntegerField()
    description = models.TextField()
    gmapsurl = models.URLField(max_length=500)

    def __str__(self):
        return self.name
