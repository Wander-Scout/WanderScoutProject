from django.db import models
from django.contrib.auth.models import User
from tourist_attraction.models import TouristAttraction
from restaurant.models import Restaurant  # Assuming you have a Restaurant model
import uuid

# Cart model for each user to collect selected attractions/restaurants
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links the cart to the user
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets the date/time when the cart is created

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "items": [item.to_dict() for item in self.items.all()],  # Serialize related items
        }


    def __str__(self):
        return f"Cart #{self.id} for {self.user}"  # Gives a friendly description of the cart

# CartItem model for individual items in the Cart
class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique ID for each item in the cart
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")  # Connects the item to its cart
    attraction = models.ForeignKey(TouristAttraction, on_delete=models.CASCADE, null=True, blank=True)  # Links to an attraction if added
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)  # Links to a restaurant if added
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Stores the price of each item
    is_weekend = models.BooleanField(default=False)  # Indicates if the item is for a weekend
    quantity = models.IntegerField(default=1)  # How many of this item are in the cart


    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.attraction.nama if self.attraction else self.restaurant.name,
            "price": float(self.price),
            "is_weekend": self.is_weekend,
            "quantity": self.quantity,
        }

    def __str__(self):
        # Show item name and quantity, whether it's an attraction or restaurant
        item_name = self.attraction.nama if self.attraction else self.restaurant.name
        return f"{item_name} (x{self.quantity})"

# Booking model to record completed purchases
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links booking to the user
    booking_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique booking ID for reference
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price of the booking
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets the booking date

    def __str__(self):
        return f"Booking {self.booking_id} for {self.user.username}"  # Description with booking ID and username

# BookingItem model for each item included in a booking
class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, related_name='items', on_delete=models.CASCADE)  # Connects the item to its booking
    name = models.CharField(max_length=255)  # Name of the item (could be attraction or restaurant)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per item
    quantity = models.IntegerField()  # Quantity for each item in the booking

    def __str__(self):
        # Shows item name and quantity in the context of a booking
        return f"{self.name} (x{self.quantity}) in booking {self.booking.booking_id}"
