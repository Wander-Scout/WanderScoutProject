import uuid  # To generate unique booking IDs
from django.shortcuts import render, get_object_or_404, redirect
from tourist_attraction.models import TouristAttraction  # Model for tourist attractions
from datetime import datetime  # For checking the current day (weekday or weekend)
from django.http import JsonResponse  # For sending JSON responses, mostly for AJAX
from .models import Cart, CartItem, Booking, BookingItem  # Models related to shopping cart and booking
from django.views.decorators.http import require_http_methods  # To limit views to specific HTTP methods
from authentication.decorators import allowed_users  # Custom decorator to limit access by user roles
from restaurant.models import Restaurant  # Model for restaurant items


@allowed_users(['tourist', 'admin'])  # Only let 'tourist' or 'admin' users in
@require_http_methods(["POST"])  # Only allow POST requests here
def add_to_cart(request, item_id):
    # Get or create a Cart for this user
    cart, created = Cart.objects.get_or_create(user=request.user)
    item_type = request.POST.get('item_type', 'attraction')  # Default to 'attraction' if not specified

    # Handle adding either an attraction or a restaurant item to the cart
    if item_type == 'attraction':  # If it's a tourist attraction
        item = get_object_or_404(TouristAttraction, id=item_id)  # Make sure it exists
        today = datetime.today().weekday()  # Get the day of the week (0=Monday, 6=Sunday)
        # Set price based on whether today is a weekday or weekend
        price = item.htm_weekday if today < 5 else item.htm_weekend
        # Add the item to the cart with its price and whether it’s a weekend
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            attraction=item,
            defaults={'price': price, 'is_weekend': today >= 5}
        )
    elif item_type == 'restaurant':  # If it's a restaurant
        item = get_object_or_404(Restaurant, id=item_id)  # Make sure the restaurant exists
        price = item.average_price  # Use the restaurant's average price
        # Add the restaurant to the cart with its price
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            restaurant=item,
            defaults={'price': price}
        )
    else:
        # If an invalid type was given, return an error message
        return JsonResponse({'success': False, 'error': 'Invalid item type'}, status=400)

    # If the item already exists in the cart, just increase the quantity
    if not created:
        cart_item.quantity += 1
    cart_item.save()  # Save the updated cart item

    # If it's an AJAX request, return a simple success message
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    # Otherwise, just redirect them to view their cart
    return redirect('view_cart')


@allowed_users(['tourist', 'admin'])  # Only allow 'tourist' or 'admin' users
@require_http_methods(["GET"])  # Only allow GET requests here
def view_cart(request):
    # Try to get the user's cart; if none, set it to None
    cart = Cart.objects.filter(user=request.user).first()

    # If they have a cart, calculate the total price from all items
    if cart:
        items = cart.items.all()
        total_price = sum(item.price * item.quantity for item in items)
    else:
        items = []  # No cart, no items
        total_price = 0  # And total price is 0

    # If this was an AJAX request, send the cart data as JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_items = {
            str(item.id): {
                'id': str(item.id),
                'name': item.attraction.nama if item.attraction else item.restaurant.name,  # Attraction or restaurant name
                'price': item.price,
                'quantity': item.quantity,
                'is_weekend': item.is_weekend if item.attraction else None,  # Only relevant for attractions
                'total_item_price': item.price * item.quantity,
                'item_type': 'attraction' if item.attraction else 'restaurant'
            }
            for item in items
        }
        return JsonResponse({
            'cart_items': cart_items,
            'total_price': total_price,
        })

    # Render the cart page, passing in items and total price
    context = {
        'cart_items': items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


@allowed_users(['tourist', 'admin'])  # Limit access to 'tourist' or 'admin' users
@require_http_methods(["POST"])  # Only POST requests allowed
def remove_from_cart(request, item_id):
    cart = Cart.objects.filter(user=request.user).first()  # Try to get the user's cart

    if cart:
        try:
            # Try to get the CartItem by its ID and cart
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()  # Delete the item from the cart
            # Send back a success response if AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            # Return an error if this was an AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)

    # If no cart was found or the request was unauthorized, return an error
    return JsonResponse({'success': False, 'error': 'Bad Request'}, status=400)


@allowed_users(['tourist', 'admin'])  # Only 'tourist' or 'admin' users allowed
@require_http_methods(["POST"])  # Only POST requests allowed here
def checkout_view(request):
    # Try to get the user's cart, or set it to None if they don't have one
    cart = Cart.objects.filter(user=request.user).first()

    # If the cart is empty, return an error message
    if not cart or not cart.items.exists():
        return JsonResponse({'error': 'Your cart is empty'}, status=400)

    items = list(cart.items.all())  # Get all items in the cart
    total_price = sum(item.price * item.quantity for item in items)  # Calculate total price
    new_booking_id = uuid.uuid4()  # Generate a new, unique booking ID

    # Create a new Booking for the user
    booking = Booking.objects.create(
        user=request.user,
        booking_id=new_booking_id,
        total_price=total_price
    )

    # Loop through each cart item and create a BookingItem for it
    for item in items:
        name = item.attraction.nama if item.attraction else item.restaurant.name
        BookingItem.objects.create(
            booking=booking,
            name=name,
            price=item.price,
            quantity=item.quantity
        )

    # Clear out the cart after checkout
    cart.items.all().delete()

    # Render the checkout page with booking info
    context = {
        'cart_items': items,
        'total_price': total_price,
        'booking_id': new_booking_id,
    }
    return render(request, 'checkout.html', context)



@allowed_users(['tourist', 'admin'])  # Only 'tourist' or 'admin' users allowed
@require_http_methods(["GET"])  # Only GET requests allowed here
def search_booking_view(request):
    booking_id = request.GET.get('booking_id')  # Get the booking_id from the request

    if booking_id:
        try:
            # Try to find the booking by ID, make sure it belongs to the user
            booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
            items = booking.items.all()  # Get all items for this booking
            
            # Render the receipt page with booking details
            return render(request, 'booking_receipt.html', {
                'booking': booking,
                'items': items
            })
        except Booking.DoesNotExist:
            # If the booking doesn't exist, show an error message
            return render(request, 'booking_receipt.html', {
                'error_message': 'Booking not found. Please check the booking ID.'
            })

    # If no booking_id was provided, just redirect to the cart
    return redirect('view_cart')

##final project

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Cart

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_view_cart(request):
    # Debug: Log the Authorization header
    print("Authorization header received:", request.headers.get("Authorization"))

    try:
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({"cart": cart.to_dict()})
    except Cart.DoesNotExist:
        return JsonResponse({"error": "Cart not found for this user."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)


