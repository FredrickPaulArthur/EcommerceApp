from django.urls import path, include
from django.urls import reverse_lazy
from . import views



app_name = "Cart"

urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    path("add/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path("buy_now/<slug:slug>/", views.buy_now, name="buy_now"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    # Remove product from cart
    # Increase/decrease quantity of a product in cart
    # Save item for later column
    # Checkout redirection
]