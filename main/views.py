from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CustomerReview
from .forms import CustomerReviewForm
from image_display.models import ImageModel
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404


@login_required(login_url='authentication:login')
def landing_page(request):
    return render(request, 'landing_page.html')

def home_page(request):
    images = ImageModel.objects.all()
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

@login_required(login_url='authentication:login')
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


@require_http_methods(["POST"])
def delete_customer_review(request, review_id):
    review = get_object_or_404(CustomerReview, id=review_id, user=request.user)
    review.delete()
    rating_filter = request.GET.get('rating', '')
    return HttpResponseRedirect(f"{reverse('display_customer_reviews')}?rating={rating_filter}")