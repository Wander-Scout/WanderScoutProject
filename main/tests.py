from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomerReview
from django.utils import timezone

class CustomerReviewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='password123')

    def test_home_page(self):
        response = self.client.get(reverse('home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_page.html')

    def test_display_customer_reviews(self):
        CustomerReview.objects.create(
            user=self.user,
            review_text='Test review',
            rating=4,
            created_at=timezone.now()
        )
        response = self.client.get(reverse('display_customer_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test review')
