from django.test import TestCase, Client
from django.urls import reverse
from .models import Restaurant
from django.contrib.auth.models import User
import uuid
import json

class DeleteRestaurantViewTest(TestCase):
    def setUp(self):
        # Create an admin user for authentication
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )
        self.client = Client()
        self.client.login(username="admin", password="adminpass")

        # Create a test restaurant
        self.restaurant = Restaurant.objects.create(
            id=uuid.uuid4(),
            name="Test Restaurant",
            food_preference="Italian",
            average_price=20,
            rating=4.5,
            atmosphere="Cozy",
            food_variety="Pasta"
        )

    def test_delete_restaurant(self):
        # URL for deleting the restaurant
        url = reverse('delete_restaurant', args=[self.restaurant.id])

        # Send a GET request to the delete_restaurant view
        response = self.client.get(url)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True, "message": "Restaurant deleted successfully"})

        # Verify that the restaurant was deleted
        with self.assertRaises(Restaurant.DoesNotExist):
            Restaurant.objects.get(id=self.restaurant.id)

class AddRestaurantViewTest(TestCase):
    def setUp(self):
        # Create an admin user for authentication
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )
        self.client = Client()
        self.client.login(username="admin", password="adminpass")

    def test_add_restaurant(self):
        url = reverse('add_restaurant')  # Ensure this matches the name in your urls.py

        restaurant_data = {
            'name': 'New Test Restaurant',
            'food_preference': 'Mexican',
            'average_price': 25,
            'rating': 4.8,
            'atmosphere': 'Vibrant',
            'food_variety': 'Tacos, Burritos'
        }

        # Send a POST request to the add_restaurant view with JSON data
        response = self.client.post(url, data=json.dumps(restaurant_data), content_type='application/json')

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)  # Expecting a 200 OK for success
        self.assertJSONEqual(response.content, {"success": True, "message": "Restaurant added successfully!", "restaurant": response.json()['restaurant']})

        # Verify that the restaurant was added to the database
        self.assertTrue(Restaurant.objects.filter(name='New Test Restaurant').exists())