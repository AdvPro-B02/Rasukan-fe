from django.urls import path
from buy.views import show_main

app_name = 'buy'

urlpatterns = [
    path('', show_main, name='show_main'),
]