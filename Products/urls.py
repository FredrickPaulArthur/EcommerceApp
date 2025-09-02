from django.urls import path, include
from . import views


app_name = "Products"
urlpatterns = [
    # Product URLs
    path("", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),

    # Category URLs
    path("categories/", views.category_list, name="category_list"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),

    # Brand URLs
    path("brands/", views.brand_list, name="brand_list"),
    path("brands/<int:pk>/", views.brand_detail, name="brand_detail"),
]