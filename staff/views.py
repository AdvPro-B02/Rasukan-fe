from django.http import JsonResponse
from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

link_order = 'http://34.87.46.220/order'
link_topup = 'http://34.87.46.220/api/topup'
LSP_URL = "http://34.87.46.220:80"
link = 'http://34.87.180.11:80/Buyer'

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
    return render(request, "manage_payment.html", context)

def manage_topup(request):
    response = requests.get(f'{link_topup}')
    topups = response.json()
    context = {
        'topups': topups,
    }
    return render(request, "manage_topup.html", context)

def update_topup_status(request, topup_id, new_status):
    if request.method == 'PUT':
        url = f'{link_topup}/{topup_id}?status={new_status}'
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
        response = requests.delete(url)

        if response.status_code == 200:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

def staff_all_listings(request):
    response = requests.get(f'{link}/listing/all')
    if response.status_code == 200:
        listings = response.json()
        
        is_staff = request.COOKIES.get('staff') 
        
        staff = is_staff == 'true'
        context = {
            'listings': listings,
            'staff': staff  
        }

        return render(request, "staff_all_listings.html", context)
    else:
        return JsonResponse({'error': 'Failed to fetch listings'}, status=500)
    
def mark_listing_as_featured(request, id):
    if request.method == 'POST':
        response = requests.post(f'{LSP_URL}/staff/listing/{id}/featured')

        if response.status_code == 200:
            return JsonResponse({'success': True, 'message': response.text})
        else:
            return JsonResponse({'error': 'No data received from backend or invalid JSON'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def remove_featured_status(request, id):
    if request.method == 'POST':
        response = requests.delete(f'{LSP_URL}/staff/listing/{id}/featured')

        if response.status_code == 200:
            return JsonResponse({'success': True, 'message': response.text})
        else:
            print(response.content) 
            return JsonResponse({'error': 'No data received from backend or invalid JSON'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def staff_featured_listings(request):
    response = requests.get(f'{LSP_URL}/staff/listing/featured')
    if response.status_code == 200:
        featured_listings = response.json()
        for listing in featured_listings:
            listing_id = listing['listingId']
            detail_response = requests.get(f'{link}/listing/get/{listing_id}')
            if detail_response.status_code == 200:
                listing_detail = detail_response.json()
                listing.update(listing_detail)
            else:
                listing['price'] = 'N/A'
                listing['stock'] = 'N/A'
                listing['seller'] = 'N/A'
        return render(request, "staff_featured_listings.html", {'featured_listings': featured_listings})
    else:
        return JsonResponse({'error': 'Failed to fetch featured listings'}, status=500)
