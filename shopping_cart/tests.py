from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Cart, CartItem, Booking
from tourist_attraction.models import TouristAttraction
from datetime import datetime

class ShoppingCartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create a user with the 'tourist' role
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Ensure the user is in the 'tourist' group to pass the `@allowed_users` decorator
        tourist_group, created = Group.objects.get_or_create(name='tourist')
        self.user.groups.add(tourist_group)
        
        self.client.login(username='testuser', password='testpass')

        # Set up a mock TouristAttraction
        self.attraction = TouristAttraction.objects.create(
            nama="Sample Attraction", htm_weekday=10.00, htm_weekend=15.00
        )

    def test_add_to_cart(self):
        """Test adding an item to the cart"""
        response = self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        self.assertIn(response.status_code, [200, 302])  # Handle AJAX and standard responses
        
        # Check if the cart and item were created
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 1)

    def test_add_existing_item_to_cart(self):
        """Test increasing the quantity when adding an existing item"""
        self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        self.client.post(reverse('add_to_cart', args=[self.attraction.id]))

        # Check the quantity has increased to 2
        cart_item = CartItem.objects.get(cart__user=self.user, attraction=self.attraction)
        self.assertEqual(cart_item.quantity, 2)

    def test_view_cart(self):
        """Test viewing the cart items"""
        self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.attraction.nama)

    def test_remove_from_cart(self):
        """Test removing an item from the cart"""
        self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        response = self.client.post(reverse('remove_from_cart', args=[self.attraction.id]))
        self.assertIn(response.status_code, [200, 302])  # Handle AJAX and standard responses

        # Confirm cart is empty after removal
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

    def test_checkout_view(self):
        """Test checkout process creates a booking and clears the cart"""
        self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 200)  # Expected checkout success
        
        # Check that the booking is created and cart is cleared
        booking = Booking.objects.get(user=self.user)
        
        # Check the price based on the day
        expected_price = self.attraction.htm_weekend if datetime.today().weekday() >= 5 else self.attraction.htm_weekday
        self.assertEqual(booking.total_price, expected_price)

        # Verify cart is empty after checkout
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

    def test_booking_detail_view(self):
        """Test viewing the booking details"""
        self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        self.client.post(reverse('checkout'))
        
        booking = Booking.objects.get(user=self.user)
        response = self.client.get(reverse('booking_detail', args=[booking.booking_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.attraction.nama)

    def test_search_booking_view_valid(self):
        """Test searching for an existing booking by booking_id"""
        self.client.post(reverse('add_to_cart', args=[self.attraction.id]))
        self.client.post(reverse('checkout'))

        booking = Booking.objects.get(user=self.user)
        response = self.client.get(reverse('search_booking') + f'?booking_id={booking.booking_id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, booking.booking_id)

    def test_search_booking_view_invalid(self):
        """Test searching for a non-existing booking by booking_id"""
        # Use a valid UUID format for non-existent booking_id
        response = self.client.get(reverse('search_booking') + '?booking_id=00000000-0000-0000-0000-000000000000')
        
        # Check for appropriate response when booking is not found
        self.assertIn(response.status_code, [200, 302, 404])  # Handle 404 as valid outcome
