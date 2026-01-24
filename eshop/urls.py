from django.urls import path
from . import views

app_name = 'eshop'

urlpatterns = [
    path('', views.product_in_category, name='product_list'),
    path('<int:category_id>/', views.product_in_category, name='product_list'),
    path('<int:id>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_details, name='cart_details'),
    path('cart/add/<int:product_id>/', views.cart_add_product, name='cart_add_product'), # type: ignore
    path('/cart/remove/<int:product_id>/', views.cart_remove_product, name='cart_remove_product'),
]
