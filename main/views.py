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


# delete Customer Review View
@allowed_users(['tourist'])  # ensure only 'tourist' users can delete reviews
@require_http_methods(["POST"])  # only allow POST requests
def delete_customer_review(request, review_id):
    review = get_object_or_404(CustomerReview, id=review_id, user=request.user)
    # get the review by ID, ensuring it belongs to the current user

    review.delete()  # delete the review
    rating_filter = request.GET.get('rating', '')  # get the current rating filter
    return HttpResponseRedirect(f"{reverse('display_customer_reviews')}?rating={rating_filter}")
    # redirect back to the reviews page, retaining the current rating filter


# add Admin Reply View
@allowed_users(['admin'])  # ensure only 'admin' users can access this view
@require_http_methods(["POST"])  # only allow POST requests
@user_passes_test(lambda u: u.is_staff)  # double-check that the user is staff
def add_admin_reply(request, review_id):
    review = get_object_or_404(CustomerReview, id=review_id)  # find the review by ID
    reply_text = request.POST.get('reply_text', '')  # get the reply text from POST data

    AdminReply.objects.create(
        review=review,
        admin=request.user,  # associate reply with the admin user
        reply_text=reply_text
    )

    return redirect('display_customer_reviews')  # redirect back to the reviews page

def show_review_json(request):
    data = CustomerReview.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import CustomerReview

@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

        try:
            data = json.loads(request.body)

            # Create the review entry
            new_review = CustomerReview.objects.create(
                user=request.user,  # Assign the logged-in user
                review_text=data["review_text"], 
                rating=int(data["rating"]),
            )

            new_review.save()

            return JsonResponse({"status": "success"}, status=200)
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
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def fetch_reviews(request):
    if request.method == "GET":
        reviews = CustomerReview.objects.all()
        review_list = [
            {
                "id": review.id,
                "username": review.user.username if review.user else "Anonymous",  # Default to "Anonymous"
                "review_text": review.review_text,
                "rating": review.rating,
                "created_at": review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for review in reviews
        ]
        return JsonResponse(review_list, safe=False)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)
