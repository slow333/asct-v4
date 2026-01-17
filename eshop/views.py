from django.shortcuts import render
from .models import Category, Product
from django.core.paginator import Paginator

def product_in_category(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    
    if category_slug:
        current_category = Category.objects.get(slug=category_slug)
        products = products.filter(category=current_category)

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    return render(request, 'eshop/list.html', {
        'current_category': current_category,
        'categories': categories,
        'page_obj': products,
    })

def product_detail(request, id, product_slug=None):
    product = Product.objects.get(id=id, slug=product_slug)

    return render(request, 'eshop/detail.html', {
        'product': product,
    })

