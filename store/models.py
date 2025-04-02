from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200)      # Product name (e.g., "Blue Shirt")
    price = models.DecimalField(...)            # Price tag
    digital = models.BooleanField(default=False) # Is it downloadable? (No physical shipping)
    image = models.ImageField()                 # Product photo
