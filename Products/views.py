from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Brand



""" Product Views """
def product_list(request):
    products = Product.objects.filter(is_available=True)
    context = {"products": products}
    return render(request, "Products/product_list.html", context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    context = {"product": product}
    return render(request, "Products/product_detail.html", context)


""" Category Views """
def category_list(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "Products/category_list.html", context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_available=True)
    context = {"category": category, "products": products}
    return render(request, "Products/category_detail.html", context)


""" Brand Views """
def brand_list(request):
    brands = Brand.objects.all()
    context = {"brands": brands}
    return render(request, "Products/brand_list.html", context)

def brand_detail(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    products = Product.objects.filter(brand=brand, is_available=True)
    context = {"brand": brand, "products": products}
    return render(request, "Products/brand_detail.html", context)