from django.db import models
from django.utils.text import slugify
import os



def upload_to_category_folder(instance, filename):
    category_name = instance.category.name if instance.category else "uncategorized"
    category_slug = slugify(category_name)
    ext = filename.split('.')[-1]
    filename = f"{instance.title}.{ext}"

    return os.path.join("products", category_slug, filename)





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
    name = models.CharField(max_length=25)
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
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to=upload_to_category_folder,
        blank=True,
        null=True,
        default='products/default/default.jpg'  # Make sure this file exists in your media directory
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_on"]
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)

        # Generate slug after initial save to access `id`
        if creating and not self.slug:
            slug_base = f"{self.title}-{self.brand.name if self.brand else ''}-{self.id}"
            self.slug = slugify(slug_base)
            self.save(update_fields=["slug"])
    
    @property
    def image_or_default_url(self):
        if self.image:
            return self.image.url

    def get_final_price(self):
        """Return discounted price if available"""
        return self.discounted_price if self.discounted_price else self.price