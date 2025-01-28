from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255)

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='Image/')
    description = models.CharField(max_length=255)
    price = models.FloatField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)