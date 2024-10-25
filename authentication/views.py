from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from authentication.decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

@require_http_methods(["GET"])
@unauthenticated_user
def display_register_form(request):
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@require_http_methods(["POST"])
@unauthenticated_user
def submit_register_form(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        username = form.cleaned_data.get('username')

        try:
            group = Group.objects.get(name='tourist')
            user.groups.add(group)
        except Group.DoesNotExist:
            messages.error(
                request,
                "The 'tourist' group does not exist. Please contact support.",
            )
            return redirect('authentication:display_register_form')

        messages.success(
            request, f'Account created for {username}! You can now log in.'
        )
        return redirect('authentication:login')
    else:
        messages.error(request, "Invalid registration details.")
    return render(request, 'register.html', {'form': form})
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

@require_http_methods(["POST"])
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('authentication:login')