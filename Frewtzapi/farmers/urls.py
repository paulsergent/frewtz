from django.urls import path
from .views import farmer_profile, farmer_create, FarmerProfileUpdate

urlpatterns = [
    path('profile/create', farmer_create.as_view(), name='farmer-create'),
    path('profile/', farmer_profile, name='farmer-profile'),
    path('profile/update/', FarmerProfileUpdate.as_view(), name='farmer-profile-update')
]