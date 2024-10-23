from django.urls import path
from .views import fetch_rss_items

urlpatterns = [
    path('rss/', fetch_rss_items, name='rss_feed'),
]
