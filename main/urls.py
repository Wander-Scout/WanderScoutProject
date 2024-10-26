from django.urls import path, include
from django.contrib import admin
from . import views
from .views import display_customer_reviews, submit_customer_review


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home_page, name='home_page'),
    path('reviews/', views.display_customer_reviews, name='display_customer_reviews'),
    path('reviews/submit/', views.submit_customer_review, name='submit_customer_review'),
    path('admin/', admin.site.urls),
    path('reviews/delete/<int:review_id>/', views.delete_customer_review, name='delete_customer_review'),    path('image_display/', include('image_display.urls')), 
]