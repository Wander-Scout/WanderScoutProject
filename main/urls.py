from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),  
    # the default home page URL. if someone visits the root URL ('/'), they get the home page

    path('home/', views.home_page, name='home_page'), 
    # an alternative way to access the home page, specifically at '/home/'

    path('reviews/', views.display_customer_reviews, name='display_customer_reviews'),
    # this URL maps to the reviews page where users can see all the customer reviews

    path('reviews/submit/', views.submit_customer_review, name='submit_customer_review'),
    # this one handles the form submission for adding a new customer review

    path('reviews/<int:review_id>/reply/', views.add_admin_reply, name='add_admin_reply'),
    # admins can reply to a specific review. the <int:review_id> part means the URL needs a review ID

    path('reviews/delete/<int:review_id>/', views.delete_customer_review, name='delete_customer_review'),
    # this URL allows deleting a specific review, using the review ID
    path('create-flutter/', views.create_review_flutter, name='create_review_flutter'),
    path('json/', views.fetch_reviews, name='fetch_reviews'),
]
