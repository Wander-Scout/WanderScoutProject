from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from .models import CustomerReview, AdminReply
from .forms import CustomerReviewForm, AdminReplyForm
from image_display.models import RSSItem
from authentication.decorators import allowed_users
from image_display.views import fetch_and_store_rss_items
from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

# Home Page View
@login_required(login_url='authentication:login')  # make sure the user is logged in
@require_http_methods(["GET"])  # only allow GET requests for this view
def home_page(request):
    # get and store RSS feed items for the home page
    fetch_and_store_rss_items()  
    images = RSSItem.objects.all().order_by('-pub_date')  # get the images, sorted by date

    return render(request, 'home_page.html', {'images': images})  
    # render the home page template and pass the images to it


# display Customer Reviews View
@require_http_methods(["GET"])  # only allow GET requests
def display_customer_reviews(request):
    rating_filter = request.GET.get('rating', '')  # get rating filter from the query params
    
    # if a rating filter is applied, filter reviews by rating; otherwise, show all reviews
    if rating_filter:
        reviews = CustomerReview.objects.filter(rating=rating_filter).order_by('-created_at')
    else:
        reviews = CustomerReview.objects.all().order_by('-created_at')
    
    form = CustomerReviewForm()  # create an empty review form for users to submit reviews
    
    return render(request, 'customer_reviews.html', {
        'form': form,
        'reviews': reviews,
        'rating_filter': rating_filter
    })
    # render the customer reviews template with the form, reviews, and current rating filter


# submit Customer Review View
@allowed_users(['tourist'])  # Ensure only users with the 'tourist' role can access this view
@require_http_methods(["POST"])  # Only allow POST requests
def submit_customer_review(request):
    if not request.user.is_authenticated:  # Ensure user is authenticated
        return JsonResponse({"message": "User not authenticated"}, status=401)

    form = CustomerReviewForm(request.POST)  # Create a form instance with POST data
    
    if form.is_valid():
        review = form.save(commit=False)  # Save the review, but don't commit yet
        review.user = request.user  # Associate the review with the logged-in user
        
        review.review_text = strip_tags(form.cleaned_data['review_text'])  # Sanitize review text
        review.save()  # Save the review to the database

        response_data = {
            'username': request.user.username,  # Include username in the response
            'review_text': review.review_text,
            'rating': review.rating,
            'created_at': review.created_at.strftime('%B %d, %Y, %I:%M %p'),
            'message': 'Your review has been submitted!',
        }
        return JsonResponse(response_data, status=201)  # Send a success response as JSON
    else:
        return JsonResponse({'message': 'Form submission error', 'errors': form.errors.as_json()}, status=400)

def show_review_json(request):
    data = CustomerReview.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import CustomerReview


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_review_flutter(request):
    try:
        data = request.data  # DRF request object handles parsing

        # Create the review entry
        new_review = CustomerReview.objects.create(
            user=request.user,  # Assign the logged-in user
            review_text=data["review_text"], 
            rating=int(data["rating"]),
        )

        new_review.save()

        return JsonResponse({"status": "success"}, status=201)
    except KeyError as e:
        return JsonResponse(
            {"status": "error", "message": f"Missing key: {str(e)}"},
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=500
        )
        
        

from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator

from .models import CustomerReview, AdminReply

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator

from .models import CustomerReview, AdminReply

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fetch_reviews(request):
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 5)

    reviews = CustomerReview.objects.all().order_by('-created_at')
    paginator = Paginator(reviews, page_size)
    page_obj = paginator.get_page(page_number)

    review_list = [
        {
            "id": review.id,
            "username": review.user.username if review.user else "Anonymous",
            "review_text": review.review_text,
            "rating": review.rating,
            "created_at": review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "admin_replies": [
                {
                    "reply_text": reply.reply_text,
                    "admin_username": reply.admin.username,
                    "created_at": reply.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for reply in AdminReply.objects.filter(review=review)
            ],
        }
        for review in page_obj.object_list
    ]

    response = {
        'reviews': review_list,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'page_number': page_obj.number,
        'total_pages': paginator.num_pages,
    }

    return JsonResponse(response, safe=False)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_admin_reply(request, review_id):
    if not request.user.is_staff:  # Ensure the user is an admin
        return JsonResponse({'error': 'Only admins can reply to reviews.'}, status=403)

    review = get_object_or_404(CustomerReview, id=review_id)
    reply_text = request.data.get('reply_text', '')

    if not reply_text:
        return JsonResponse({'error': 'Reply text is required.'}, status=400)

    AdminReply.objects.create(
        review=review,
        admin=request.user,
        reply_text=reply_text,
    )

    return JsonResponse({'message': 'Reply added successfully.'}, status=201)

from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_if_admin(request):
    """Check if the logged-in user is an admin."""
    is_admin = request.user.is_staff  # Django's default flag for admin users
    return JsonResponse({'is_admin': is_admin})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomerReview

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_customer_review(request, review_id):
    # Retrieve the review and ensure it belongs to the currently authenticated user
    review = get_object_or_404(CustomerReview, id=review_id, user=request.user)
    
    review.delete()
    return Response({"message": "Review deleted successfully."}, status=204)
