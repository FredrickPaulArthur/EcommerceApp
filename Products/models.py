from django.db import models
from django.utils.text import slugify
from datetime import datetime
import os
from django.urls import reverse




def upload_to_category_folder(instance, filename):
    category_name = instance.category.name if instance.category else "uncategorized"
    category_slug = slugify(category_name)
    ext = filename.split('.')[-1]
    filename = f"{instance.title}.{ext}"

    return os.path.join("products", category_slug, filename)

def validate_manufacture_date(value):
    try:
        # Validate that the date matches the 'DD-MM-YYYY' format
        datetime.strptime(value, "%d-%m-%Y")
    except ValueError:
        raise ValueError(f"{value} is not a valid date format. Use DD-MM-YYYY.")




class Brand(models.Model):
    name = models.CharField(max_length=32, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Brands"
    
    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=45)
    slug = models.SlugField(unique=True, max_length=120)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, db_index=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image_path = models.CharField(
        max_length=500, default="product_images/default.jpg",
        help_text="Path in B2 bucket, e.g. 'product_images/default.jpg'"
    )
    manufactured_date = models.CharField(max_length=10, validators=[validate_manufacture_date], blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_on"]
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        creating = self.pk is None  # Check if the object is being created (not updated)
        
        # If we're creating a new product, generate the slug after initial save
        if creating and not self.slug:
            slug_base = f"{self.title}-{self.brand.name if self.brand else ''}-{self.id}"
            self.slug = slugify(slug_base)
        
        # Convert manufactured_on date if it's a string
        if isinstance(self.manufactured_date, str):
            try:
                self.manufactured_date = datetime.strptime(self.manufactured_date, "%d-%m-%Y").date()
            except ValueError:
                self.manufactured_date = None  # or handle the error accordingly

        # Perform the actual save (either create or update)
        super().save(*args, **kwargs)
        
        # If slug was generated after the initial save, update the slug
        if creating and self.slug:
            self.save(update_fields=["slug"])  # Update only the slug field

    @property
    def display_image_url(self):
        """
        Returns a URL to fetch the product image from the private B2 bucket via Django view.
        """
        return reverse("Products:product_image", kwargs={"product_id": self.id})

    @property
    def final_price(self):
        """Return discounted price if available, else normal price"""
        return self.price