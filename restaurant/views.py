from django.shortcuts import render
from django.urls import path
from django.http import JsonResponse
from .models import Restaurant

# Create your views here.
def get_all_restaurants(request):
    restaurants = Restaurant.objects.all().values('name', 'food_preference', 'average_price', 'rating', 'atmosphere_type', 'food_variations')
    return JsonResponse(list(restaurants), safe=False)