from django.shortcuts import render
from .models import Category, Product
from django.core.paginator import Paginator

def product_in_category(request):
    products = Product.objects.all()
    
    category_list = list(Category.objects.all().values('name')) 
    # 각 카테고리별 게시글 수 집계
    # [{'name': '카테고리1', 'count': 5}, {'name': '카테고리2', 'count': 3}, ...]
    for cat in category_list:
        cat['count'] = Product.objects.filter(category__name=cat['name']).count()
    current_category = request.GET.get('category')

    if current_category:
        current_category = Category.objects.get(name=current_category)
        products = products.filter(category__name=current_category)
    print(products)

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    return render(request, 'eshop/list.html', {
        'current_category': current_category,
        'category_list': category_list,
        'page_obj': products,
    })

def product_detail(request, id, product_slug=None):
    product = Product.objects.get(id=id, slug=product_slug)

    return render(request, 'eshop/detail.html', {
        'product': product,
    })

