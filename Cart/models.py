from django.db import models
from Products.models import Product
from Accounts.models import CustomUser



class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    session_key = models.CharField(max_length=40, blank=True) 

    class Meta:
        ordering = ["-added_at"]
        verbose_name_plural = "Cart Items"
    
    def __str__(self):
        return f"{self.quantity} of {self.product.title} for {self.user.username}"
    
    def total_price(self):
        return self.quantity * self.product.price



class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField(CartItem, related_name="carts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Carts"
    
    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def total_cost(self):
        return sum(item.total_price() for item in self.items.all())