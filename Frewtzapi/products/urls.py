from django.urls import path
from .views import ProductCreate, ProductUpdate, product_delete, ProductDetail
from django.conf.urls.static import static
from Frewtzapi import settings

urlpatterns = [
    path('create/', ProductCreate.as_view(), name="product-create"),
    path('<slug:slug>/', ProductDetail.as_view(), name="product-detail" ),
    path('update/<str:slug>/', ProductUpdate.as_view(), name='product-update'),
    path('delete/<str:slug>/', product_delete, name='product-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
