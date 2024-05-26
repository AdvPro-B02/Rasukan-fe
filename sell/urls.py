from django.urls import path
from sell.views import *

app_name = 'sell'

urlpatterns = [
    path('orders', manage_orders, name='manage_orders'),
    path('update-order-status/<str:order_id>/<str:new_status>/', update_order_status, name='update_order_status'),
]