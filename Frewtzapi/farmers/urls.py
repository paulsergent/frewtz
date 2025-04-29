from django.urls import path
from .views import farmer_profile, FarmerCreate, FarmerProfileUpdate, farmers_list, farmer_search, farmer_order_history, farmer_order_history  
from django.conf.urls.static import static
from Frewtzapi import settings

urlpatterns = [
    path('', farmers_list, name='farmers-list'),
    path('profile/create', FarmerCreate.as_view(), name='farmer-create'),
    path('profile/', farmer_profile, name='farmer-profile'),
    path('profile/update/', FarmerProfileUpdate.as_view(), name='farmer-profile-update'),
    path('search/', farmer_search, name='farmer-search'),
    path('farmer/orders/history/', farmer_order_history, name='farmer-order-history'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)