from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing_page.html') 

def home_page(request):
    return render(request, 'home_page.html')