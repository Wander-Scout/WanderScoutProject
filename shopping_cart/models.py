from django.db import models
from django.contrib.auth.models import User
from tourist_attraction.models import TouristAttraction
from restaurant.models import Restaurant  # Assuming you have a Restaurant model
import uuid

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.id} for {self.user}"

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Use UUID as primary key
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    attraction = models.ForeignKey(TouristAttraction, on_delete=models.CASCADE, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_weekend = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        item_name = self.attraction.nama if self.attraction else self.restaurant.name
        return f"{item_name} (x{self.quantity})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.booking_id} for {self.user.username}"

class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.name} (x{self.quantity}) in booking {self.booking.booking_id}"
