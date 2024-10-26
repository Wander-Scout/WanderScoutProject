from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from authentication.decorators import unauthenticated_user, allowed_users, admin_only
from django.http import HttpResponse

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        # Initial setup before each test
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "password123"
        self.user = User.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )

    def test_user_registration(self):
        # Testing user registration endpoint
        response = self.client.post(reverse('authentication:submit_register_form'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Assuming redirect on success
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        # Testing user login
        response = self.client.post(reverse('authentication:submit_login_form'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # Redirects on successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_login(self):
        # Testing login with invalid credentials
        response = self.client.post(reverse('authentication:submit_login_form'), {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Typically returns 200 with error message
        self.assertIn("Invalid username or password", response.content.decode())  # Check error message

    def test_logout(self):
        # Testing logout functionality
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('authentication:logout_user'))
        self.assertEqual(response.status_code, 302)  # Redirects on logout
        response = self.client.get(reverse('authentication:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)  # Ensure user is logged out

class DecoratorTests(TestCase):
    def setUp(self):
        # Create a factory to simulate requests
        self.factory = RequestFactory()

        # Set up users with different roles
        self.user = User.objects.create_user(username="testuser", password="password")
        self.admin_user = User.objects.create_user(username="adminuser", password="password")
        self.tourist_user = User.objects.create_user(username="touristuser", password="password")

        # Create or retrieve groups to avoid IntegrityError
        admin_group, _ = Group.objects.get_or_create(name="admin")
        tourist_group, _ = Group.objects.get_or_create(name="tourist")

        # Assign groups to users
        self.admin_user.groups.add(admin_group)
        self.tourist_user.groups.add(tourist_group)



    def test_unauthenticated_user_decorator_allows_unauthenticated_user(self):
        # Test that an unauthenticated user is allowed by unauthenticated_user decorator
        request = self.factory.get('/')
        request.user = AnonymousUser()  # Using AnonymousUser to simulate an unauthenticated user

        @unauthenticated_user
        def view(request):
            return HttpResponse("This is the view")

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"This is the view")

    def test_allowed_users_decorator_allows_user_in_group(self):
        # Test that a user in an allowed group can access the view
        request = self.factory.get('/')
        request.user = self.admin_user

        @allowed_users(allowed_roles=['admin'])
        def view(request):
            return HttpResponse("Admin view")

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Admin view")

    def test_allowed_users_decorator_denies_user_not_in_group(self):
        # Test that a user not in an allowed group is denied access
        request = self.factory.get('/')
        request.user = self.tourist_user

        @allowed_users(allowed_roles=['admin'])
        def view(request):
            return HttpResponse("Admin view")

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"You are not authorized to view this page")

    def test_admin_only_decorator_allows_admin_user(self):
        # Test that an admin user can access the view
        request = self.factory.get('/')
        request.user = self.admin_user

        @admin_only
        def view(request):
            return HttpResponse("Admin only view")

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Admin only view")



    def test_admin_only_decorator_denies_user_not_in_any_group(self):
        # Test that a user not in any group is denied access
        request = self.factory.get('/')
        request.user = self.user  # User without any group

        @admin_only
        def view(request):
            return HttpResponse("Admin only view")

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"You are not authorized to view this page")