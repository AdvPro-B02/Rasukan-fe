import json
from django.http import JsonResponse
from django.shortcuts import render
import requests

link_order = 'http://34.87.46.220/order'

# Create your views here.
def manage_orders(request):
    userID = request.session.get('id') 

    response = requests.get(f'{link_order}/seller/{userID}')

    try:
        orders = response.json()
    except json.decoder.JSONDecodeError:
        message = "Seller tidak punya order."
        return render(request, "sell.html", {'message': message})
    
    orders = response.json()
    
    context = {
        'orders': orders,
    }
    print(orders)
    return render(request, "sell.html", context)

def update_order_status(request, order_id, new_status):
    if request.method == 'PATCH':
        url = f'{link_order}/{order_id}/update-order-status?newOrderStatus={new_status}'
        print(url)
        response = requests.patch(url)

        if response.status_code == 200:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
        