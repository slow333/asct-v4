from typing import Any, Iterable
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    # SEO를 위한 필드
    meta_description = models.TextField(null=True, blank=True)
    # 다양한 언어 허용(allow_unicode)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
        
    def __str__(self) -> str:
        return self.name
    def get_absolute_url(self):
        return reverse("eshop:product_in_category", args=[self.slug])
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    
    name= models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True,null=True, default='products/no-image.jpg')
    made_by = models.CharField(max_length=200, db_index=True, default='Unknown')

    description = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)    
    stock = models.PositiveSmallIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-category', 'name']
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self) -> str:
        return self.name
    def get_absolute_url(self):
        return reverse("eshop:product_detail", args=[self.id, self.slug]) # type: ignore
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
