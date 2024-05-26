from django.urls import path
from buy.views import *

app_name = 'buy'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('listing/all', all_listings, name='all_listings'),
    path('listing/create/', create_listing, name="create_listing"),
    path('listing/edit/', edit_listing, name="edit_listing"),
    path('listing/by_me', see_my_listings, name='see_my_listings'),
    path("cart/", see_cart, name='see_cart'),
    path("cart/add", add_to_cart, name='add_to_cart'),
    path("cart/remove", remove_from_cart, name='remove_from_cart'),
    path("cart/checkout/", checkout, name='checkout'),
]