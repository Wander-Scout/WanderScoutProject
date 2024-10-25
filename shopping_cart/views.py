import uuid
from django.shortcuts import render, get_object_or_404, redirect
from tourist_attraction.models import TouristAttraction
from datetime import datetime
from django.http import JsonResponse
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, attraction_id):
    # Get or create the current user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get the attraction directly without converting it to UUID
    attraction = get_object_or_404(TouristAttraction, id=attraction_id)

    # Determine if it's a weekday or weekend
    today = datetime.today().weekday()  # Monday is 0, Sunday is 6
    price = attraction.htm_weekday if today < 5 else attraction.htm_weekend

    # Add the attraction to the cart, or update the quantity if it already exists
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, attraction=attraction,
        defaults={'price': price, 'is_weekend': today >= 5}
    )
    
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})  # Return success as JSON for AJAX

    # If not an AJAX request, redirect to view_cart
    return redirect('view_cart')


@login_required
def view_cart(request):
    # Get the cart for the current user, or return an empty cart
    cart = Cart.objects.filter(user=request.user).first()
    
    if cart:
        items = cart.items.all()
        total_price = sum(item.price * item.quantity for item in items)
    else:
        items = []
        total_price = 0

    # Handle AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Build cart data for JSON response
        cart_items = {
            str(item.attraction.id): {  # Ensure the ID is passed
                'id': str(item.attraction.id),  # Add ID here
                'name': item.attraction.nama,
                'price': item.price,
                'quantity': item.quantity,
                'is_weekend': item.is_weekend,
                'total_item_price': item.price * item.quantity,
            }
            for item in items
        }
        return JsonResponse({
            'cart_items': cart_items,
            'total_price': total_price,
        })

    # If not an AJAX request, render the full cart page
    context = {
        'cart_items': items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


@login_required
def remove_from_cart(request, attraction_id):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_item = CartItem.objects.filter(cart=cart, attraction__id=attraction_id).first()
        if cart_item:
            cart_item.delete()

    # Return JSON response if it's an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})  # Return success response

    # Otherwise, redirect to the cart page if not an AJAX request
    return redirect('view_cart')


