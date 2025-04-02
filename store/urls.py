from django.urls import path
from .import views

path('', views.store, name="store")  # Map URL "/" to the store view