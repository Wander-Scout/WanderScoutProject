from django.urls import path, include
from . import views
from .views import display_customer_reviews, submit_customer_review


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home_page, name='home_page'),
    path('news/', include('news_rss.urls')),
    path('reviews/', display_customer_reviews, name='customer_reviews'),  # Make sure this matches
    path('reviews/submit/', submit_customer_review, name='submit_customer_review'),
]