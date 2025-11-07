from django.urls import path, include
from . import views
from Products.b2_helper import product_image
from django.views.decorators.cache import cache_page
app_name = "Products"



urlpatterns = [
    # Product URLs
    path("", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("product/<int:product_id>/image/", product_image, name="product_image"),

    # Category URLs
    path("categories/", views.category_list, name="category_list"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),

    # Brand URLs
    path("brands/", views.brand_list, name="brand_list"),
    # path("brands/<int:pk>/", cache_page(300)(views.brand_detail), name="brand_detail"),     # Per-view caching for 300 seconds
    path("brands/<int:pk>/", views.brand_detail, name="brand_detail"),

    # Search URLs
    path("search/", views.search_products, name="search_products"),
]