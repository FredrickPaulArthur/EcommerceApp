from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('Accounts.urls'), name='accounts'),
    # path('cart/', include('Cart.urls'), name='cart'),
    # path('orders/', include('Orders.urls'), name='orders'),
    # path('search/', include('Search.urls'), name='search'),
    # path('payments/', include('Payments.urls'), name='payments'),
    # path('wishlist/', include('Wishlist.urls'), name='wishlist'),
    # path('reviews/', include('Reviews.urls'), name='reviews'),
    # path('checkout/', include('Checkout.urls'), name='checkout'),
    path('', include('Products.urls'), name='products'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)