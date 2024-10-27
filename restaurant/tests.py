from django.test import TestCase, Client
from django.urls import reverse
from restaurant.models import Restaurant
from django.contrib.auth.models import User, Group
import uuid
import json

class DeleteRestaurantViewTest(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )
        
        # Ensure the 'admin' group exists and add the user to it
        admin_group, created = Group.objects.get_or_create(name="admin")
        self.admin_user.groups.add(admin_group)
        
        # Log in the client as the admin user
        self.client = Client()
        self.client.login(username="admin", password="adminpass")

        # Create a sample restaurant
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

        # Send a GET request to delete the restaurant
        response = self.client.get(url)

        # Check if the response is successful and JSON matches expected response
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True, "message": "Restaurant deleted successfully"})

        # Verify that the restaurant is deleted from the database
        with self.assertRaises(Restaurant.DoesNotExist):
            Restaurant.objects.get(id=self.restaurant.id)


class AddRestaurantViewTest(TestCase):
    def setUp(self):
        # Create an admin user for authentication
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )
        
        # Ensure the 'admin' group exists and add the user to it
        admin_group, created = Group.objects.get_or_create(name="admin")
        self.admin_user.groups.add(admin_group)
        
        # Log in the client as the admin user
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

        # Expected JSON response (matching the actual structure from the view)
        expected_response = {
            "success": True,
            "restaurant": response.json().get('restaurant')  # Dynamically gets the restaurant ID
        }

        # Check if the response JSON matches the expected response
        self.assertEqual(response.status_code, 200)  # Expecting a 200 OK for success
        self.assertJSONEqual(response.content, expected_response)

        # Verify that the restaurant was added to the database
        self.assertTrue(Restaurant.objects.filter(name='New Test Restaurant').exists())


class EditRestaurantViewTest(TestCase):
    def setUp(self):
        # Create an admin user for authentication
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )
        
        # Ensure the 'admin' group exists and add the user to it
        admin_group, created = Group.objects.get_or_create(name="admin")
        self.admin_user.groups.add(admin_group)
        
        # Log in the client as the admin user
        self.client = Client()
        self.client.login(username="admin", password="adminpass")

        # Create a sample restaurant
        self.restaurant = Restaurant.objects.create(
            id=uuid.uuid4(),
            name="Original Restaurant",
            food_preference="Italian",
            average_price=20,
            rating=4.5,
            atmosphere="Cozy",
            food_variety="Pasta"
        )

    def test_edit_restaurant(self):
        # URL for editing the restaurant
        url = reverse('update_restaurant', args=[self.restaurant.id])

        # Data for updating the restaurant
        updated_data = {
            'name': 'Updated Restaurant',
            'food_preference': 'Mexican',
            'average_price': 30,
            'rating': 4.2,
            'atmosphere': 'Lively',
            'food_variety': 'Tacos, Burritos'
        }

        # Send a POST request to update the restaurant with JSON data
        response = self.client.post(url, data=json.dumps(updated_data), content_type='application/json')

        # Expected JSON response structure
        expected_response = {
            "success": True
        }

        # Check if the response JSON matches the expected response
        self.assertEqual(response.status_code, 200)  # Expecting a 200 OK for success
        self.assertJSONEqual(response.content, expected_response)

        # Verify that the restaurant details were updated in the database
        self.restaurant.refresh_from_db()  # Refresh the object to get updated data
        self.assertEqual(self.restaurant.name, 'Updated Restaurant')
        self.assertEqual(self.restaurant.food_preference, 'Mexican')
        self.assertEqual(self.restaurant.average_price, 30)
        self.assertEqual(self.restaurant.rating, 4.2)
        self.assertEqual(self.restaurant.atmosphere, 'Lively')
        self.assertEqual(self.restaurant.food_variety, 'Tacos, Burritos')



    def test_edit_nonexistent_restaurant(self):
        # Test editing a restaurant that doesn't exist
        non_existent_id = uuid.uuid4()  # Generate a random UUID
        url = reverse('update_restaurant', args=[non_existent_id])
        
        updated_data = {
            'name': 'Ghost Restaurant',
            'food_preference': 'Thai',
            'average_price': 20,
            'rating': 4.0,
            'atmosphere': 'Modern',
            'food_variety': 'Noodles'
        }
        
        # Attempt to edit the non-existent restaurant
        response = self.client.post(url, data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)  # Not found status