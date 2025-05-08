from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponseForbidden
from .models import Product
from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ProductSerializer
from .permissions import IsFarmerPermission
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


# Create your views here.

def index(request):
    products = Product.objects.all()  # Fetch all products from the database

    return render(request, 'products/index.html', context={"products": products} )  # Render the template with the products context

class ProductDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(instance=product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductCreate(APIView):
    permission_classes = [permissions.IsAuthenticated, IsFarmerPermission]
    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/product_create.html'



    def get(self, request):
        serializer = ProductSerializer(context={'request': request})
        return Response({'serializer': serializer.data})

    def post(self, request):
        data = request.data.copy()
        data.update(request.FILES) # Include files in the data
        serializer = ProductSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'errors': serializer.errors, 'product': None, 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        product = serializer.save()
        
        return redirect('farmer-profile') 
        
    
    
    
    
class ProductUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated, IsFarmerPermission]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/product_update.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        user = request.user
        if product.farmer.user.pk != user.pk:
            return HttpResponseForbidden("You do not have permission to edit this product.")
        serializer = ProductSerializer(instance=product, context={'request': request})
        return Response({'serializer': serializer, 'product': product})

    
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        user = request.user
        if product.farmer.user.pk != user.pk:
            return HttpResponseForbidden("You do not have permission to edit this product.")
        data = request.POST.copy()
        data.update(request.FILES)
        serializer = ProductSerializer(instance=product, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            return redirect('farmer-profile')
        return Response({'serializer': serializer, 'product': product, 'errors': serializer.errors, 'success': False}, status=status.HTTP_400_BAD_REQUEST)
    
    
def product_delete(request, slug):
    
    permission_classes = [permissions.IsAuthenticated, IsFarmerPermission]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    product = get_object_or_404(Product, slug=slug)
    if product.farmer.pk != request.user.pk:
        return HttpResponseForbidden("You do not have permission to delete this product.")
    
    product.delete()
    return redirect('farmer-profile')
