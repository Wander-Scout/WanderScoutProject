from django.db import models
import uuid

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default="Unnamed Restaurant")
    food_preference = models.CharField(max_length=100, default="Unknown")
    average_price = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    atmosphere = models.CharField(max_length=100, default="Unknown")
    food_variety = models.CharField(max_length=255, default="Unknown")

    def __str__(self):
        return self.Nama_Restoran
