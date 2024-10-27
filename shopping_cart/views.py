import uuid  # Import uuid to generate a unique booking ID
from django.shortcuts import render, get_object_or_404, redirect
from tourist_attraction.models import TouristAttraction
from datetime import datetime
from django.http import JsonResponse
from .models import Cart, CartItem, Booking, BookingItem
from django.views.decorators.http import require_http_methods
from authentication.decorators import allowed_users
from restaurant.models import Restaurant  # Import Restaurant model


@allowed_users(['tourist', 'admin'])
@require_http_methods(["POST"])
def add_to_cart(request, item_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    item_type = request.POST.get('item_type', 'attraction')  # Default to 'attraction' if not specified

    # Determine the item type and add accordingly
    if item_type == 'attraction':
        item = get_object_or_404(TouristAttraction, id=item_id)
        today = datetime.today().weekday()
        price = item.htm_weekday if today < 5 else item.htm_weekend
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            attraction=item,
            defaults={'price': price, 'is_weekend': today >= 5}
        )
    elif item_type == 'restaurant':
        item = get_object_or_404(Restaurant, id=item_id)
        price = item.average_price
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            restaurant=item,
            defaults={'price': price}
        )
    else:
        return JsonResponse({'success': False, 'error': 'Invalid item type'}, status=400)

    # Increase quantity if the item already exists
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('view_cart')


@allowed_users(['tourist', 'admin'])
@require_http_methods(["GET"])
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        items = cart.items.all()
        total_price = sum(item.price * item.quantity for item in items)
    else:
        items = []
        total_price = 0

    # Prepare items for JSON response if AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_items = {
            str(item.id): {
                'id': str(item.id),
                'name': item.attraction.nama if item.attraction else item.restaurant.name,
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

    context = {
        'cart_items': items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

@allowed_users(['tourist', 'admin'])
@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    print(f"Attempting to remove item with ID: {item_id}")  # Debugging statement
    cart = Cart.objects.filter(user=request.user).first()
    
    if cart:
        # Attempt to find the CartItem by its primary key (UUID) directly
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
            print("Item deleted successfully")  # Debugging statement
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            print("Failed to delete item or item not found")  # Debugging statement
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)

    print("Bad Request - Cart not found or unauthorized")  # Debugging statement
    return JsonResponse({'success': False, 'error': 'Bad Request'}, status=400)



@allowed_users(['tourist', 'admin'])
@require_http_methods(["POST"])
def checkout_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart or not cart.items.exists():
        return JsonResponse({'error': 'Your cart is empty'}, status=400)

    items = list(cart.items.all())
    total_price = sum(item.price * item.quantity for item in items)
    new_booking_id = uuid.uuid4()

    booking = Booking.objects.create(
        user=request.user,
        booking_id=new_booking_id,
        total_price=total_price
    )

    for item in items:
        name = item.attraction.nama if item.attraction else item.restaurant.name
        BookingItem.objects.create(
            booking=booking,
            name=name,
            price=item.price,
            quantity=item.quantity
        )

    # Clear the cart after checkout
    cart.items.all().delete()

    context = {
        'cart_items': items,
        'total_price': total_price,
        'booking_id': new_booking_id,
    }
    return render(request, 'checkout.html', context)


@allowed_users(['tourist', 'admin'])
@require_http_methods(["GET"])
def booking_detail_view(request, booking_id):
    # Fetch the booking by booking_id and ensure it belongs to the current user
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    items = booking.items.all()

    context = {
        'booking': booking,
        'items': items
    }
    return render(request, 'booking_detail.html', context)


@allowed_users(['tourist', 'admin'])
@require_http_methods(["GET"])
def search_booking_view(request):
    # Get the booking_id from the query parameters
    booking_id = request.GET.get('booking_id')
    
    if booking_id:
        try:
            # Retrieve the booking if it exists for the logged-in user
            booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
            items = booking.items.all()  # Retrieve all items for this booking
            
            # Render the receipt page with booking details
            return render(request, 'booking_receipt.html', {
                'booking': booking,
                'items': items
            })
        except Booking.DoesNotExist:
            # If booking_id doesn't exist or doesn't belong to the user
            return render(request, 'booking_receipt.html', {
                'error_message': 'Booking not found. Please check the booking ID.'
            })

    # If no booking_id was provided, redirect to the cart page or show an error
    return redirect('view_cart')

@allowed_users(['tourist', 'admin'])
@require_http_methods(["GET"])
def past_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings
    }
    return render(request, 'past_bookings.html', context)
