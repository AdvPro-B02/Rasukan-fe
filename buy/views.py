import json
from django.shortcuts import redirect, render
import requests
from django.http import JsonResponse

# link = 'http://localhost:8080/Buyer'
link = 'http://34.87.180.11:80/Buyer'

# Create your views here.
def show_main(request):
    context = {
    }

    return render(request, "buy.html", context)

def see_cart(request):
    # userID = request.session.get('id') 
    userID = 'e3b012da-23a3-46c3-9307-23387f350d85'

    createCart = requests.get(f'{link}/cart/get/{userID}')

    response = requests.get(f'{link}/cart/get_listings/{userID}')
    listings = response.json()

    context = {
        'listings': listings,
        'ownerID' : userID,
    }

    return render(request, 'cart.html', context)



def all_listings(request):
    response = requests.get(f'{link}/listing/all')
    listings = response.json()
    # buyerID = request.session.get('id') 
    buyerID = 'e3b012da-23a3-46c3-9307-23387f350d85'

    # if (is_staff):
    #     staffId = 'true' 
    # else:
    #     staffId = 'false'
    context = {
        'listings': listings,
        'buyerID': buyerID,
        # 'staffID' : staffId
    }
    print(listings)
    return render(request, "all_listings.html", context)

def see_my_listings(request):
    # userID = request.session.get('id')
    userID = 'e3b012da-23a3-46c3-9307-23387f350d85'
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
        seller = 'e3b012da-23a3-46c3-9307-23387f350d85'
        # seller = request.session.get('id')

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
    

def edit_listing(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        # seller = request.session.get('id') 
        seller = 'e3b012da-23a3-46c3-9307-23387f350d85'

        # Update the listing details
        url = f'{link}/listing/update/{listing_id}'
        data = {
            "name": name,
            "price": price,
            "stock": stock,
            "seller": seller
        }
        response = requests.post(url, json=data)
        
        # Redirect to the 'all_listings' view
        return redirect('buy:all_listings')

    
def add_to_cart(request):
    if request.method == 'POST':

        listing_id = request.POST.get('listing_id')
        # cart_id = request.session.get('id') 
        cart_id = 'e3b012da-23a3-46c3-9307-23387f350d85'
        createCart = requests.get(f'{link}/cart/get/{cart_id}')

        # print(listing_id)
        print(cart_id)

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
        listings = []
        for listing_id in listing_ids:
            response = requests.get(f'{link}/listing/get/{listing_id}')
            listing = response.json()
            listings.append(listing)

        context = {
            'listings': listings
        }
        print(listings)
        return render(request, 'checkout.html', context)

