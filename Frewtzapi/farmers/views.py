from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import FarmerSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Farmer
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from order.models import Order

def farmers_list(request):
    farmers = Farmer.objects.all()
    return render(request, 'farmers/farmers_list.html', {'farmers': farmers})



# Create your views here.
class FarmerCreate(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication] 
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'farmers/farmer_create.html'
    def get(self, request):
        serializer = FarmerSerializer()
        return Response({'serializer': serializer})
    
    def post(self, request):
        
        serializer = FarmerSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)
        if hasattr(request.user, 'farmer_user'):
            return Response({'serializer': serializer, "message": "Farmer profile already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return redirect('farmer-profile')
    
    

def farmer_profile(request):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication] 
    user = request.user
    if request.method == 'POST':
        serializer = FarmerSerializer(user, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('farmer-profile')
    else:
        serializer = FarmerSerializer(user)
    return render(request, 'farmers/farmer_profile.html', {'serializer': serializer})
   
        

class FarmerProfileUpdate(APIView):
        
        permission_classes = [permissions.IsAuthenticated]
        authentication_classes = [SessionAuthentication, BasicAuthentication] 
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'farmers/farmer_profile_update.html'
    
        def get(self, request):
            serializer = FarmerSerializer(request.user.farmer_user)
            return Response({'serializer': serializer})
    
        def post(self, request):
            farmer = request.user.farmer_user
            data = request.data.copy()
            data.update(request.FILES)  # Include files in the data
            
            serializer = FarmerSerializer(farmer, data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return redirect('farmer-profile')
            return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)
        
def farmer_search(request):
    permission_classes = [permissions.AllowAny]
    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    query = request.GET.get('query')
    if query:
        results = Farmer.objects.filter(
            farm_name__icontains=query
        ) | Farmer.objects.filter(
            farm_location__icontains=query
        ) | Farmer.objects.filter(
            products__name__icontains=query
        )
        results = results.distinct()
    else:
        results = Farmer.objects.all()
    return render(request, 'farmers/farmer_search.html', {'results': results, 'query': query})

# def farmer_alert(request):
#     farmer = request.user.farmer_user
#     new_orders = Order.objects.filter(products__farmer=farmer, ordered=True, status='pending').distinct()
#     return render(request, 'farmers/farmer_alert.html', {'new_orders': new_orders})
    
   
def farmer_order_history(request):
    farmer = request.user.farmer_user
    orders = Order.objects.filter(product__farmer=farmer, ordered=True).order_by('-ordered_date')
    return render(request, 'farmers/farmer_order_history.html', {'orders': orders})