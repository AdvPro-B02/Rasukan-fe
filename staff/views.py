from django.http import JsonResponse
from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt

link_order = 'http://34.87.46.220/order'
link_topup = 'http://34.87.46.220/api/topup'

# Create your views here.
def show_main(request):
    context = {
    }

    return render(request, "staff.html", context)

def manage_payment(request):
    response = requests.get(f'{link_order}/')
    orders = response.json()
    context = {
        'orders': orders,
    }
    print(orders)
    return render(request, "manage_payment.html", context)

def manage_topup(request):
    response = requests.get(f'{link_topup}')
    topups = response.json()
    context = {
        'topups': topups,
    }
    print(topups)
    return render(request, "manage_topup.html", context)

def update_topup_status(request, topup_id, new_status):
    if request.method == 'PUT':
        url = f'{link_topup}/{topup_id}?status={new_status}'
        print('aaaaa')
        print(url)
        response = requests.put(url)

        if response.status_code == 200:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

def update_payment_status(request, order_id, new_status):
    if request.method == 'PATCH':
        url = f'{link_order}/{order_id}/update-payment-status?newPaymentStatus={new_status}'
        response = requests.patch(url)

        if response.status_code == 200:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

def delete_order(request, order_id):
    if request.method == 'DELETE':
        url = f'{link_order}/delete/{order_id}'
        print(url)
        response = requests.delete(url)

        if response.status_code == 200:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})