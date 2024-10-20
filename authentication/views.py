from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

# Create your views here.
@require_http_methods(["GET"])
def display_login_form(request):
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@require_http_methods(["POST"])
def submit_login_form(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Login successful.")
        return redirect('home_page')
    else:
        messages.error(request, "Invalid username or password.")
    return render(request, 'login.html', {'form': form})

@require_http_methods(["GET"])
def display_register_form(request):
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@require_http_methods(["POST"])
def submit_register_form(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()  # This saves the new user to the database
        username = form.cleaned_data.get('username')
        messages.success(request, f'Account created for {username}! You can now log in.')
        return redirect('authentication:login')  # Redirect to the login page after successful registration
    else:
        messages.error(request, "Invalid registration details.")
    return render(request, 'register.html', {'form': form})