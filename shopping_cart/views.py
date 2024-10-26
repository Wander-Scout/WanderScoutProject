import uuid  # Import uuid to generate a unique booking ID
from django.shortcuts import render, get_object_or_404, redirect
from tourist_attraction.models import TouristAttraction
from datetime import datetime
from django.http import JsonResponse
from .models import Cart, CartItem, Booking, BookingItem
from django.views.decorators.http import require_http_methods
from authentication.decorators import allowed_users

@allowed_users(['tourist', 'admin'])
@require_http_methods(["POST"])
def add_to_cart(request, attraction_id):
    cart, created = Cart.objects.get_or_create(user=request.user)

    attraction = get_object_or_404(TouristAttraction, id=attraction_id)
    today = datetime.today().weekday()
    price = attraction.htm_weekday if today < 5 else attraction.htm_weekend

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, attraction=attraction,
        defaults={'price': price, 'is_weekend': today >= 5}
    )

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

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_items = {
            str(item.attraction.id): {
                'id': str(item.attraction.id),
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

    context = {
        'cart_items': items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

@allowed_users(['tourist', 'admin'])
@require_http_methods(["POST"])
def remove_from_cart(request, attraction_id):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_item = CartItem.objects.filter(cart=cart, attraction__id=attraction_id).first()
        if cart_item:
            cart_item.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('view_cart')

@allowed_users(['tourist', 'admin'])
@require_http_methods(["POST"])
def checkout_view(request):
    # Get the user's cart
    cart = Cart.objects.filter(user=request.user).first()
    
    # Ensure cart exists and has items
    if not cart or not cart.items.exists():
        return JsonResponse({'error': 'Your cart is empty'}, status=400)

    # Retrieve cart items and calculate total price
    items = list(cart.items.all())
    total_price = sum(item.price * item.quantity for item in items)

    # Generate a unique booking_id for the new Booking instance
    new_booking_id = uuid.uuid4()

    # Create a new Booking instance for this checkout with a new booking_id
    booking = Booking.objects.create(
        user=request.user,
        booking_id=new_booking_id,
        total_price=total_price
    )

    # Create BookingItem instances for each item in the cart
    for item in items:
        BookingItem.objects.create(
            booking=booking,
            name=item.attraction.nama,
            price=item.price,
            quantity=item.quantity
        )

    # Clear the cart after checkout
    cart.items.all().delete()

    # Pass the data to the template
    context = {
        'cart_items': items,
        'total_price': total_price,
        'booking_id': new_booking_id,  # Use the new booking_id
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
