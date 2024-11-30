from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from authentication.decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from .forms import ProfileForm
from .models import Profile
from django.http import JsonResponse
from django.utils.html import strip_tags

@require_http_methods(["GET"])
@unauthenticated_user
def display_register_form(request):
    # show the registration form page
    # this is a GET request (loads the form for users to fill in)
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@require_http_methods(["POST"])
@unauthenticated_user
def submit_register_form(request):
    # process the registration form data when user submits it
    # uses POST to handle form submission
    form = UserCreationForm(request.POST)
    if form.is_valid():
        # save the new user
        user = form.save()
        
        # sanitize the username to prevent XSS attacks
        username = strip_tags(form.cleaned_data.get('username'))
        user.username = username  # update the username after sanitizing
        user.save()

        # add the new user to the "tourist" group
        try:
            group = Group.objects.get(name='tourist')
            user.groups.add(group)
        except Group.DoesNotExist:
            # handle case where "tourist" group isn't found
            messages.error(
                request,
                "The 'tourist' group does not exist. Please contact support.",
            )
            return redirect('authentication:display_register_form')

        # show a success message and redirect to login page
        messages.success(
            request, f'Account created for {username}! You can now log in.'
        )
        return redirect('authentication:login')
    else:
        # if form data is invalid, show an error and reload registration form
        messages.error(request, "Invalid registration details.")
    return render(request, 'register.html', {'form': form})

@require_http_methods(["GET"])
def display_login_form(request):
    # show the login form page
    # uses GET to load the form
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@require_http_methods(["POST"])
def submit_login_form(request):
    # handle login when user submits their credentials
    # uses POST to process login data
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        # if valid, log the user in and redirect to home page
        user = form.get_user()
        login(request, user)
        messages.success(request, "Login successful.")
        return redirect('home_page')
    else:
        # show error if login fails and reload login form
        messages.error(request, "Invalid username or password.")
    return render(request, 'login.html', {'form': form})

@require_http_methods(["POST"])
@login_required
def logout_user(request):
    # log the user out
    # uses POST to handle logout action
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('authentication:login')

@allowed_users(['tourist', 'admin'])
@login_required
@require_http_methods(["GET"])
def display_edit_profile_page(request):
    # show the profile edit page
    # uses GET to load the page
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@allowed_users(['tourist', 'admin'])
@login_required
@require_http_methods(["GET"])
def display_edit_profile(request):
    # send current profile data as JSON to the frontend
    # uses GET to fetch profile data (usually for AJAX requests)
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile)
    
    # create a dictionary with form field names and values
    form_data = {field.name: field.value() for field in form}
    
    return JsonResponse({'success': True, 'form_data': form_data})

@allowed_users(['tourist', 'admin'])
@login_required
@require_http_methods(["POST"])
def submit_edit_profile(request):
    # handle profile edits submitted by the user
    # uses POST to update profile data (often used with AJAX)
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST, instance=profile)

    if form.is_valid():
        # sanitize profile fields to prevent XSS
        profile_instance = form.save(commit=False)
        profile_instance.address = strip_tags(profile_instance.address)
        profile_instance.phone_number = strip_tags(profile_instance.phone_number)
        
        # save sanitized data
        profile_instance.save()
        
        return JsonResponse({'success': True})
    else:
        # send back form errors if validation fails
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

#-----------------------------------#
# Start of Final Project

from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.contrib.auth import logout as auth_logout
from rest_framework.authtoken.models import Token

@csrf_exempt
def flutter_login(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({
                "status": True,
                "message": "Login successful!",
                "username": user.username,
                "token": token.key,
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Invalid username or password.",
            }, status=401)
    return JsonResponse({
        "status": False,
        "message": "Invalid request method.",
    }, status=400)
    
@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)

        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # Add the new user to the "tourist" group
        try:
            group = Group.objects.get(name='tourist')
            user.groups.add(group)
        except Group.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "The 'tourist' group does not exist. Please contact support."
            }, status=400)

        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully and added to 'tourist' group!"
        }, status=200)

    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def flutter_logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout failed."
        }, status=401)