from django.db import models
from django.utils import timezone
from django.urls import reverse
from farmers.models import Farmer


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    price = models.FloatField(default=0.0)
    stock = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to='products', blank=True, null=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='products', default=None)  # ForeignKey field to link the product to a farmer. The on_delete=models.CASCADE argument specifies that if the related farmer is deleted, all their products should also be deleted.
    created_at = models.DateTimeField(default=timezone.now)  # Automatically set the field to now when the object is first created.
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # This method returns the name of the product and creates a name-tag for this model
        return f"{self.name} ({self.stock}) from {self.farmer}"
    
    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})  # This method returns the URL of the product detail page based on the slug field. It uses the reverse() function to generate the URL dynamically. The reverse() function takes the name of the URL pattern and any arguments needed to construct the URL. In this case, it takes the slug field as an argument.

    
