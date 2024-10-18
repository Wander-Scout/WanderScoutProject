from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods



@login_required(login_url='authentication:login')
def landing_page(request):
    return render(request, 'landing_page.html') 

def home_page(request):
    return render(request, 'home_page.html')





    