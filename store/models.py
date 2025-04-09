from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False)  # No shipping needed
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    
    @property
    def get_cart_total(self):
        return sum([item.get_total for item in self.orderitem_set.all()])
    
    @property
    def get_cart_items(self):
        return sum([item.quantity for item in self.orderitem_set.all()])

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    
    @property
    def get_total(self):
        return self.product.price * self.quantity
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)