from django.urls import path
from staff.views import show_main

app_name = 'staff'

urlpatterns = [
    path('', show_main, name='show_main'),
]