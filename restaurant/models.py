from django.db import models
import uuid

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Nama_Restoran = models.CharField(max_length=255, default="Unnamed Restaurant")
    Preferensi_Makanan = models.CharField(max_length=100, default="Unknown")
    Harga_Rata_Rata_Makanan_di_Toko = models.IntegerField(default=0)
    Rating_Toko = models.FloatField(default=0.0)
    Jenis_Suasana = models.CharField(max_length=100, default="Unknown")
    Variasi_Makanan = models.CharField(max_length=255, default="Unknown")

    def __str__(self):
        return self.Nama_Restoran
