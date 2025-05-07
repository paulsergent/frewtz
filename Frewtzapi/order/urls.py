from django.urls import path
from .views import add_to_cart, cart, delete_cart, confirm_order, OrderActionView, customer_order_history, customer_confirm_delivery
from django.conf.urls.static import static
from Frewtzapi import settings


urlpatterns = [
    path('<str:slug>/add-to-cart', add_to_cart, name="add-to-cart" ),
    path('cart', cart, name="cart" ),
    path('cart/delete', delete_cart, name="delete-cart" ),
    path('orders/action/<int:pk>/', OrderActionView.as_view(), name='handle-order-action'),
    path('cart/confirm', confirm_order, name='confirm-order'),
    path('orders/history/', customer_order_history, name='customer-order-history'),
    path('orders/confirm_delivery/<int:pk>/', customer_confirm_delivery, name='confirm-delivery'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
