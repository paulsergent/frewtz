from django.db import models
from Frewtzapi.settings import AUTH_USER_MODEL
from products.models import Product
from django.utils import timezone



# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name}  ({self.quantity})"
    
class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    

    def __str__(self):
        return self.user.email

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
        self.orders.clear()  # Clear the ManyToMany field before deleting the cart

        super().delete(*args, **kwargs)
    