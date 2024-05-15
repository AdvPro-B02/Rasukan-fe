from django.urls import path
from sell.views import show_main

app_name = 'sell'

urlpatterns = [
    path('', show_main, name='show_main'),
]