from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import CustomerReview
from .forms import CustomerReviewForm

@login_required(login_url='authentication:login')
def landing_page(request):
    return render(request, 'landing_page.html') 

def home_page(request):
    return render(request, 'home_page.html')

@require_http_methods(["POST"])
def customer_reviews(request):
    if request.method == 'POST':
        form = CustomerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted!")
            return redirect('customer_reviews')
    else:
        form = CustomerReviewForm()

    reviews = CustomerReview.objects.all().order_by('-created_at')
    return render(request, 'customer_reviews.html', {'form': form, 'reviews': reviews})
