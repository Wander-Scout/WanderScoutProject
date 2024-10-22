from django.urls import path
from . import views
from .views import customer_reviews



urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home_page, name='home_page'),
    path('reviews/', customer_reviews, name='customer_reviews'),
]