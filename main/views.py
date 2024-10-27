from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import CustomerReview, AdminReply
from .forms import CustomerReviewForm, AdminReplyForm
from image_display.models import RSSItem
from authentication.decorators import allowed_users
from image_display.views import fetch_and_store_rss_items


@login_required(login_url='authentication:login')
def landing_page(request):
    return render(request, 'landing_page.html')

@require_http_methods(["GET"])
def home_page(request):
    #Fetch all the data from the rss feed
    fetch_and_store_rss_items()  
    images = RSSItem.objects.all().order_by('-pub_date')  

    return render(request, 'home_page.html', {'images': images})  


@require_http_methods(["GET"])
def display_customer_reviews(request):
    rating_filter = request.GET.get('rating', '')
    
    if rating_filter:
        reviews = CustomerReview.objects.filter(rating=rating_filter).order_by('-created_at')
    else:
        reviews = CustomerReview.objects.all().order_by('-created_at')
    
    form = CustomerReviewForm()
    
    return render(request, 'customer_reviews.html', {
        'form': form,
        'reviews': reviews,
        'rating_filter': rating_filter
    })

@allowed_users(['tourist'])
@require_http_methods(["POST"])
def submit_customer_review(request):
    form = CustomerReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            response_data = {
                'username': request.user.username,
                'review_text': review.review_text,
                'rating': review.rating,
                'created_at': review.created_at.strftime('%B %d, %Y, %I:%M %p')
            }
            return JsonResponse(response_data) 
        
        messages.success(request, "Your review has been submitted!")
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'There was an error in your submission.'}, status=400)
        messages.error(request, "There was an error in your submission.")
    
    return redirect('display_customer_reviews')

@allowed_users(['tourist'])
@require_http_methods(["POST"])
def delete_customer_review(request, review_id):
    review = get_object_or_404(CustomerReview, id=review_id, user=request.user)
    review.delete()
    rating_filter = request.GET.get('rating', '')
    return HttpResponseRedirect(f"{reverse('display_customer_reviews')}?rating={rating_filter}")


@allowed_users(['admin'])
@require_http_methods(["POST"])
def add_admin_reply(request, review_id):
    review = get_object_or_404(CustomerReview, id=review_id)
    form = AdminReplyForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.review = review
        reply.admin = request.user
        reply.save()
        messages.success(request, "Reply has been added!")
    else:
        messages.error(request, "Error adding reply.")
    
    rating_filter = request.GET.get('rating', '')
    return HttpResponseRedirect(f"{reverse('display_customer_reviews')}?rating={rating_filter}")