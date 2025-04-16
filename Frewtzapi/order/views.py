from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from products.models import Product
from .models import Cart, Order
from django.urls import reverse

# Create your views here.
def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user,
                                                 ordered=False,
                                                 product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()
    return redirect(reverse("product", kwargs={"slug": slug})) 

def cart(request):

    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'cart.html', context={"orders": cart.orders.all()}) 

def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()
    return redirect('index')