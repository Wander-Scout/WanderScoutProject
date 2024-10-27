from django.urls import path
from .views import fetch_and_store_rss_items

urlpatterns = [
    path('fetch-and-store-rss-items/', fetch_and_store_rss_items, name='fetch_and_store_rss_items'),
]
