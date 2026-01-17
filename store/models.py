from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    def __str__(self) -> str:
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='store/images/', blank=True)

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    address = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=[('P', 'Pending'), ('C', 'Complete'), ('F', 'Failed')], default='P')
    
    def __str__(self) -> str:
        return self.product.name