from django.db import models
from users.models import User



# Create your models here.
class Farmer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_user')
    farm_name = models.CharField(max_length=255, blank=True, null=True)
    farm_location = models.CharField(max_length=255, blank=True, null=True)
    # farm_type = models.CharField(max_length=255, blank=True, null=True)  # e.g., organic, conventional
    farm_description = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='farmers/', blank=True, null=True)

    def __str__(self):
        return self.farm_name or self.user.email
