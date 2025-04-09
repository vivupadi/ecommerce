from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.conf import settings
import stripe

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    
    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)

from django.shortcuts import redirect

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create the order
    order, created = Order.objects.get_or_create(
        customer=request.user,
        complete=False
    )
    
    # Get or create the order item
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )
    
    if not created:
        order_item.quantity += 1
        order_item.save()
    
    return redirect('store')  # Redirect back to store page

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    
    context = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', context)

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def process_order(request):
    if request.method == 'POST':
        # Process payment
        try:
            charge = stripe.Charge.create(
                amount=int(float(request.POST['total']) * 100),  # cents
                currency='usd',
                source=request.POST['stripeToken']
            )
            # Mark order as complete
            order = Order.objects.get(id=int(request.POST['order_id']))
            order.complete = True
            order.save()
        except stripe.error.CardError as e:
            return JsonResponse({'error': e.user_message})
    return redirect('store')