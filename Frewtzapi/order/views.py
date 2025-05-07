from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from products.models import Product
from .models import Cart, Order
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import OrderActionSerializer
from products.permissions import IsFarmerPermission


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
    return render(request, 'order/cart.html', context={"orders": cart.orders.all()}) 

def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()
    return redirect('index')

def confirm_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.delete()
    return redirect('index')  # Redirect to the index page after confirming the order

def place_order(request, slug):
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

def customer_order_history(request):
    orders = Order.objects.filter(user=request.user, ordered=True).order_by('-ordered_date')
    return render(request, 'order/customer_order_history.html', {'orders': orders})

class OrderActionView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsFarmerPermission]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order/handle_order.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.product.farmer.user != request.user:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderActionSerializer(order)
        return Response({'order': order, 'serializer': serializer})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.product.farmer.user != request.user:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        action = request.data.get('action')
        if action == 'accept':
            order.status = 'accepted'
            order.save()
        elif action == 'reject':
            order.status = 'rejected'
            order.save()
        elif action == 'deliver':
            if order.quantity > order.product.stock:
                return Response({'detail': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)
            order.status = 'on_delivery'
            order.product.stock -= order.quantity
            order.product.save()
            order.save()
        return redirect('farmer-order-history')
    
    
    
def customer_confirm_delivery(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.user != request.user:
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    action = request.POST.get('action')
    if action == 'delivered':
        order.status = 'delivered'
        order.save()
    return redirect('customer-order-history')