from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import TouristAttraction
import json

class TouristAttractionTestCase(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create an 'admin' group and assign it to the admin user
        self.admin_group, _ = Group.objects.get_or_create(name='admin')
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpass')
        self.admin_user.groups.add(self.admin_group)

        # Create a sample tourist attraction
        self.attraction = TouristAttraction.objects.create(
            nama='Sample Attraction',
            rating=4.5,
            vote_average=4.5,
            vote_count=100,
            type='Museum',
            htm_weekday=10.0,
            htm_weekend=15.0,
            description='A fascinating place to explore.',
            gmaps_url='https://maps.google.com',
            latitude=-6.200000,
            longitude=106.816666,
        )

    def test_delete_attraction_as_admin(self):
        # Admin user can delete an attraction
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.delete(
            reverse('delete_tourist_attraction', args=[self.attraction.id]),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(TouristAttraction.objects.filter(id=self.attraction.id).exists())

    def test_create_attraction_as_admin(self):
        # Admin user can create an attraction
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.post(
            reverse('add_tourist_attraction'),
            data=json.dumps({
                "nama": "New Attraction",
                "rating": 4.8,
                "vote_average": 4.8,
                "vote_count": 20,
                "type": "Park",
                "htm_weekday": 12.0,
                "htm_weekend": 18.0,
                "description": "A beautiful new attraction.",
                "gmaps_url": "https://maps.google.com",
                "latitude": -6.300000,
                "longitude": 106.900000,
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(TouristAttraction.objects.filter(nama="New Attraction").exists())

    def test_edit_attraction_as_admin(self):
            # Admin user can edit an attraction
            self.client.login(username='adminuser', password='adminpass')
            response = self.client.post(
                reverse('edit_tourist_attraction', args=[self.attraction.id]),
                data=json.dumps({
                    "nama": "Updated Attraction",
                    "rating": 4.9
                }),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            
            # Refresh from the database and check if the values were updated
            self.attraction.refresh_from_db()
            self.assertEqual(self.attraction.nama, "Updated Attraction")
            self.assertEqual(self.attraction.rating, 4.9)
