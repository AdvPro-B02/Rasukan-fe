from django.urls import path
from staff.views import *

app_name = 'staff'

urlpatterns = [
    path('payment', manage_payment, name='manage_payment'),
    path('topup', manage_topup, name='manage_topup'),
    path('update-topup-status/<str:topup_id>/<str:new_status>/', update_topup_status, name='update_topup_status'),
    path('update-payment-status/<str:order_id>/<str:new_status>/', update_payment_status, name='update_payment_status'),
    path('delete/<str:order_id>', delete_order, name='delete_order'),
]