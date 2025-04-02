from django.shortcuts import render
from django.store.models import *

# Create your views here.

def store(request):
    products = Product.objects.all()  # Grab all products from the "shelf"
    return render(request, 'store/store.html', {'products': products})
