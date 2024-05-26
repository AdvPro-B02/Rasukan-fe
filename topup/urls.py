from django.urls import path
from topup.views import topup_main, get_topup, create_topup, delete_topup, delete_all_topup

app_name = 'topup'

urlpatterns = [
    path('', topup_main, name='topup_main'),
    path('get/', get_topup, name='get_topup'),
    path('delete/<str:id>', delete_topup, name='delete_topup'),
    path('delete-all/', delete_all_topup, name='delete_all_topup'),
    path('create/', create_topup, name='create_topup'),
]