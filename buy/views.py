import json
from django.shortcuts import redirect, render
import requests
from django.http import JsonResponse

# link = 'http://localhost:8080/Buyer'
link = 'http://34.87.180.11:80/Buyer'
link_order = 'http://34.87.46.220/order'
LSP_URL = "http://34.87.46.220:80"

# Create your views here.
def show_main(request):
    context = {
    }

    return render(request, "buy.html", context)

def see_cart(request):
    userID = request.session.get('id') 

    createCart = requests.get(f'{link}/cart/get/{userID}')

    response = requests.get(f'{link}/cart/get_listings/{userID}')
    listings = response.json()

    context = {
        'listings': listings,
        'ownerID' : userID,
    }

    return render(request, 'cart.html', context)


def all_listings(request):
    all_listings_response = requests.get(f'{link}/listing/all')
    if all_listings_response.status_code == 200:
        all_listings = all_listings_response.json()

        featured_response = requests.get(f'{LSP_URL}/staff/listing/featured')
        if featured_response.status_code == 200:
            featured_listings = featured_response.json()
        else:
            return JsonResponse({'error': 'Failed to fetch featured listings'}, status=500)

        featured_ids = set()

        for listing in featured_listings:
            listing_id = listing['listingId']
            detail_response = requests.get(f'{link}/listing/get/{listing_id}')
            if detail_response.status_code == 200:
                listing_detail = detail_response.json()
                listing.update(listing_detail)
                featured_ids.add(listing_id)
            else:
                listing['price'] = 'N/A'
                listing['stock'] = 'N/A'
                listing['seller'] = 'N/A'

        displayed_listings = featured_listings.copy()

        for listing in all_listings:
            if listing['listingId'] not in featured_ids:
                displayed_listings.append(listing)

        buyerID = request.session.get('id')
        context = {
            'listings': displayed_listings,
            'buyerID': buyerID,
        }
        return render(request, "all_listings.html", context)
    else:
        return JsonResponse({'error': 'Failed to fetch all listings'}, status=500)

def featured_listings(request):
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
        return render(request, "featured_listings.html", {'featured_listings': featured_listings})
    else:
        return JsonResponse({'error': 'Failed to fetch featured listings'}, status=500)


def see_my_listings(request):
    userID = request.session.get('id')
    # userID = 'e3b012da-23a3-46c3-9307-23387f350d85'
    response = requests.get(f'{link}/listings/by_seller/{userID}')
    listings = response.json()

    context = {
        'listings': listings,
        'sellerID': userID,
        'buyerID': userID,
    }
    return render(request, "all_listings.html", context)

def create_listing(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        # seller = 'e3b012da-23a3-46c3-9307-23387f350d85'
        seller = request.session.get('id')

        urll = f'{link}/listing/create'
        # headers = {'Authorization': 'Your Token Here'}
        data = {
            "name": name,
            "price": price,
            "stock": stock,
            "seller": seller
        }
        response = requests.post(urll, json=data)
        
        return redirect('buy:all_listings')
    else:
        return render(request, 'create_listing.html')
    

# def edit_listing(request):
#     if request.method == 'POST':
#         listing_id = request.POST.get('listing_id')
#         name = request.POST.get('name')
#         price = request.POST.get('price')
#         stock = request.POST.get('stock')
#         seller = request.session.get('id') 
#         # seller = 'e3b012da-23a3-46c3-9307-23387f350d85'

#         # Update the listing details
#         url = f'{link}/listing/update/{listing_id}'
#         data = {
#             "name": name,
#             "price": price,
#             "stock": stock,
#             "seller": seller
#         }
#         response = requests.post(url, json=data)
        
#         # Redirect to the 'all_listings' view
#         return redirect('buy:all_listings')

def edit_listing(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        seller = request.session.get('id')

        # Update the listing details
        url = f'{link}/listing/update/{listing_id}'
        data = {
            "name": name,
            "price": price,
            "stock": stock,
            "seller": seller
        }
        response = requests.post(url, json=data)

        if response.status_code == 200:
            # Return a success message or the updated listing details as JSON
            return JsonResponse({'success': True, 'message': 'Listing updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to update listing'})

    
def add_to_cart(request):
    if request.method == 'POST':

        listing_id = request.POST.get('listing_id')
        cart_id = request.session.get('id') 
        # cart_id = 'e3b012da-23a3-46c3-9307-23387f350d85'
        createCart = requests.get(f'{link}/cart/get/{cart_id}')

        # print(listing_id)


        urll = f'{link}/cart/add/{cart_id}/{listing_id}'
        # print(url)
        headers = {'Authorization': 'Your Token Here'}
        response = requests.post(urll, headers=headers)
        

        return redirect('buy:see_cart')
    
def remove_from_cart(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        owner_id = request.POST.get('owner_id')
        # print(listing_id)
        # print(owner_id)

        url = f'{link}/cart/remove/{owner_id}/{listing_id}'
        # print(url)
        headers = {'Authorization': 'Your Token Here'}
        response = requests.delete(url, headers=headers)

        return redirect('buy:see_cart')
    
    
def checkout(request):
    if request.method == 'POST':
        listing_ids = request.POST.getlist('listingcheckout[]')
        userId = request.session.get('id')
        nominal = request.POST.get('overall_total')
        notes = request.POST.get('notes')
        discount= request.POST.get('discount')

        listings = []
        listingQuantityMap = {}
        for listing_id in listing_ids:
            response = requests.get(f'{link}/listing/get/{listing_id}')
            listing = response.json()
            seller = listing.get('seller')
            listings.append(listing)
        listingQuantities = request.POST.getlist('hidden_amounts[]')
        for i, listing_id in enumerate(listing_ids):
            listingQuantityMap[listing_id] = listingQuantities[i]

        url = f'{link_order}/checkout'
        # headers = {'Authorization': 'Your Token Here'}
        if len(notes)!=0 and len(discount)!=0:
            data = {
                "userId": userId,
                "nominal": nominal,
                "discount": discount,
                "notes": notes,
                "seller": seller,
                "listingQuantityMap": listingQuantityMap
            }
        elif len(notes)==0 and len(discount)!=0:
            data = {
                "userId": userId,
                "nominal": nominal,
                "discount": discount,
                "seller": seller,
                "listingQuantityMap": listingQuantityMap
            }
        elif len(notes)!=0 and len(discount)==0 :
            data = {
                "userId": userId,
                "nominal": nominal,
                "notes": notes,
                "seller": seller,
                "listingQuantityMap": listingQuantityMap
            }
        else:
            data = {
                "userId": userId,
                "nominal": nominal,
                "seller": seller,
                "listingQuantityMap": listingQuantityMap
            }
        response = requests.post(url, json=data)
        
        context = {
            'listings': listings
        }

        return render(request, 'checkout.html', context)

