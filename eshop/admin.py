from django.contrib import admin
from .models import Category, Product
from django.db import models as model
from django.contrib.admin.options import StackedInline

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'made_by', 'price', 'stock', 'image']
    list_filter = ['created', 'updated', 'category']
    list_editable = ['price', 'stock']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']




