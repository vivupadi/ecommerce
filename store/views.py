from django.shortcuts import render
from .models import *

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

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    orderItem.quantity += 1
    orderItem.save()
    return redirect('store')

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