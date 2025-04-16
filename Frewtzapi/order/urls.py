from django.urls import path
from .views import add_to_cart, cart, delete_cart
from django.conf.urls.static import static
from Frewtzapi import settings


urlpatterns = [
    path ('<str:slug>/add-to-cart', add_to_cart, name="add-to-cart" ),
    path ('cart', cart, name="cart" ),
    path ('cart/delete', delete_cart, name="delete-cart" ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
