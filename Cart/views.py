from django.shortcuts import render






def view_cart(request):
    user = request.user
    cart = None
    if user.is_authenticated:
        cart = getattr(user, 'Cart', None)

    context = {
        "cart": cart,
    }
    return render(request, "Cart/view_cart.html", context)



def add_to_cart(request, slug):
    # Logic to add product to cart
    pass



def buy_now(request, slug):
    # Logic to buy product immediately
    pass



def remove_from_cart(request, item_id):
    # Logic to remove product from cart
    pass
