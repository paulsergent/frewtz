from django.contrib import admin
from .views import index
from django.urls import path, include
from .views import product_detail
from django.conf.urls.static import static
from Frewtzapi import settings

urlpatterns = [
    path ('<str:slug>/', product_detail, name="product" )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
