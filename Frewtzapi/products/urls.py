from django.urls import path
from .views import product_detail, ProductCreate, ProductUpdate, product_delete
from django.conf.urls.static import static
from Frewtzapi import settings

urlpatterns = [
    path('create/', ProductCreate.as_view(), name="product-create"),
    path('<str:slug>/', product_detail, name="product" ),
    path('update/<str:slug>/', ProductUpdate.as_view(), name='product-update'),
    path('delete/<str:slug>/', product_delete, name='product-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
