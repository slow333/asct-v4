from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .models import Category, Product
from .forms import AddProductForm
from .cart import Cart

def product_in_category(request):
    products = Product.objects.all()
    cart = Cart(request)
    
    category_list = list(Category.objects.all().values('name')) 
    # 각 카테고리별 게시글 수 집계
    # [{'name': '카테고리1', 'count': 5}, {'name': '카테고리2', 'count': 3}, ...]
    for cat in category_list:
        cat['count'] = Product.objects.filter(category__name=cat['name']).count()
    current_category = request.GET.get('category')

    if current_category:
        current_category = Category.objects.get(name=current_category)
        products = products.filter(category__name=current_category)

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    return render(request, 'eshop/list.html', {
        'current_category': current_category,
        'category_list': category_list,
        'page_obj': products,
        'cart': cart,
    })

def product_detail(request, id, product_slug=None):
    product= get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity': 1})
    cart = Cart(request)

    return render(request, 'eshop/product_detail.html', {
        'product': product, 'add_to_cart': add_to_cart,
        'cart': cart
    })

@require_POST
def cart_add_product(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])
        
        return redirect('eshop:cart_details')

def cart_remove_product(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('eshop:cart_details')

def cart_details(request):
    cart = Cart(request)
    for product in cart:
        product['quantity_form'] = AddProductForm(
            initial={'queantity':product['quantity'], 'is_update': True})
        print(product)
    return render(request, 'eshop/cart_details.html', {'cart': cart})