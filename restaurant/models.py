import csv
import os
from django.db import models
from django.conf import settings

# model for Restaurant
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    food_preference = models.CharField(max_length=255)
    average_price = models.FloatField()
    rating = models.FloatField()
    atmosphere_type = models.CharField(max_length=255)
    food_variations = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    # collect data, buat ngecek go to "http://localhost:8000/restaurant/get-all-restaurants/" abis dirun
    @staticmethod
    def collect_data_from_csv():
        csv_path = os.path.join(settings.BASE_DIR, 'static/data/Kuliner.csv') 
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Restaurant.objects.create(
                    name=row['Nama Restoran'],
                    food_preference=row['Preferensi Makanan'],
                    average_price=row['Harga Rata-Rata Makanan di Toko (Rp)'],
                    rating=row['Rating Toko'],
                    atmosphere_type=row['Jenis Suasana'],
                    food_variations=row['Variasi Makanan']
                )
        print(f"Data from {csv_path} successfully added to the database.")
