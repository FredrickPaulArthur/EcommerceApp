from django.contrib import admin
from .models import Product, Category, Brand

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

admin.site.register(Category)
admin.site.register(Brand)