from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Product
from django.shortcuts import get_object_or_404


# Create your views here.

def index(request):
    products = Product.objects.all()  # Fetch all products from the database

    return render(request, 'products/index.html', context={"products": products} )  # Render the template with the products context

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/detail.html', context={"product": product})
