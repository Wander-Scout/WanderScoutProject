from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    food_preference = models.CharField(max_length=100)
    average_price = models.IntegerField()
    rating = models.FloatField()
    atmosphere = models.CharField(max_length=100)
    food_variety = models.CharField(max_length=255)

    def __str__(self):
        return self.name
