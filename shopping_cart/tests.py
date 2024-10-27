from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Cart, CartItem, Booking, BookingItem
from tourist_attraction.models import TouristAttraction
from restaurant.models import Restaurant
import uuid
from datetime import datetime

class ShoppingCartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create a user with the 'tourist' role
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Ensure the user is in the 'tourist' group
        tourist_group, created = Group.objects.get_or_create(name='tourist')
        self.user.groups.add(tourist_group)
        
        self.client.login(username='testuser', password='testpass')

        # Set up a mock TouristAttraction and Restaurant
        self.attraction = TouristAttraction.objects.create(
            nama="Sample Attraction", htm_weekday=10.00, htm_weekend=15.00
        )
        self.restaurant = Restaurant.objects.create(
            name="Sample Restaurant", average_price=20.00
        )

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        self.assertIn(response.status_code, [200, 302])
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 1)

    def test_add_existing_item_to_cart(self):
        self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        cart_item = CartItem.objects.get(cart__user=self.user, attraction=self.attraction)
        self.assertEqual(cart_item.quantity, 2)

    def test_remove_from_cart(self):
        # Add an item to the cart and then remove it
        self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        cart_item = CartItem.objects.filter(cart__user=self.user).first()
        
        # Try removing the item
        response = self.client.post(reverse('remove_from_cart', args=[cart_item.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        # Confirm cart is empty after removal
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

    def test_checkout_view(self):
        self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        
        booking = Booking.objects.get(user=self.user)
        expected_price = self.attraction.htm_weekend if datetime.today().weekday() >= 5 else self.attraction.htm_weekday
        self.assertEqual(booking.total_price, expected_price)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

    def test_search_existing_booking(self):
        # Create a booking and test searching for it
        booking_id = uuid.uuid4()
        booking = Booking.objects.create(user=self.user, booking_id=booking_id, total_price=50.00)
        BookingItem.objects.create(booking=booking, name="Sample Attraction", price=10.00, quantity=1)

        response = self.client.get(reverse('search_booking'), {'booking_id': booking_id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Attraction')
