from django.db import models
from django.contrib.auth.models import User
from AppAdmin.models import Product

# Create your models here.

class Customer(models.Model):
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='Image/')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Cart(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def totalPrice(self):
        return self.quantity*self.product_id.price
