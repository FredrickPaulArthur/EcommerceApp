from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Brand
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache, cache_control, cache_page
from django.core.paginator import Paginator
from django.db.models import Q




# Product Views
def product_list(request):
    products = Product.objects.filter(is_available=True)
    pag = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = pag.get_page(page_number)

    context = {"products": products}
    return render(request, "Products/product_list.html", context)



# @cache_page(500)  # cache for 500 seconds
@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    context = {"product": product}
    return render(request, "Products/product_detail.html", context)



# Category Views
# @never_cache
def category_list(request):
    categories = Category.objects.all()
    pag = Paginator(categories, 5)
    page_number = request.GET.get('page')
    categories = pag.get_page(page_number)

    context = {"categories": categories}
    return render(request, "Products/category_list.html", context)



# @cache_control(max_age=300)
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products_of_category = Product.objects.filter(category=category, is_available=True)

    pag = Paginator(products_of_category, 12)
    page_number = request.GET.get('page')
    products_of_category = pag.get_page(page_number)

    context = {"category": category, "products": products_of_category}
    return render(request, "Products/category_detail.html", context)



# Brand Views
def brand_list(request):
    brands = Brand.objects.all()
    pag = Paginator(brands, 5)
    page_number = request.GET.get('page')
    brands = pag.get_page(page_number)

    context = {"brands": brands}
    return render(request, "Products/brand_list.html", context)



def brand_detail(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    products_of_brand = Product.objects.filter(brand=brand, is_available=True)

    pag = Paginator(products_of_brand, 12)
    page_number = request.GET.get('page')
    products_of_brand = pag.get_page(page_number)

    context = {"brand": brand, "products": products_of_brand}
    return render(request, "Products/brand_detail.html", context)



# Search View
def search_products(request):
    query = request.GET.get('product_q', '')
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),  # Added description filter
            is_available=True
        )
    else:
        products = Product.objects.none()

    pag = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = pag.get_page(page_number)

    context = {"products": products, "query": query}
    return render(request, "Products/search_results.html", context)