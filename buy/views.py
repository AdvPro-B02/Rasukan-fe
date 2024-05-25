import json
from django.shortcuts import redirect, render
import requests
from django.http import JsonResponse

link = 'http://localhost:8080/Buyer'
# link = 'http://34.87.180.11:80/Buyer'

# Create your views here.
def show_main(request):
    context = {
    }

    return render(request, "buy.html", context)

def see_cart(request):
    # cart_service = CartService()
    # cart = cart_service.get_cart(user_id)
    userID = 'ab123456-cd7e-8901-2345-678f8gh9i012'

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
    buyerID = 'be469675-cd2c-4449-8871-235f6aa9e038'

    context = {
        'listings': listings,
        'buyerID': buyerID
    }
    print(listings)
    return render(request, "all_listings.html", context)

def see_my_listings(request):
    userID = '38651b55-5d30-4bb1-87fb-e32a219addf9'
    response = requests.get(f'{link}/listings/by_seller/{userID}')
    listings = response.json()

    context = {
        'listings': listings,
        'sellerID': userID,
    }
    return render(request, "all_listings.html", context)

def create_listing(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        seller = "38651b55-5d30-4bb1-87fb-e32a219addf9"  # static seller ID

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
        # TODO: change to ID
        seller = "38651b55-5d30-4bb1-87fb-e32a219addf9"  # static seller ID

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
        cart_id = "ab123456-cd7e-8901-2345-678f8gh9i012"  # static cart ID
        # print(listing_id)
        # print(cart_id)

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
    return render(request, 'checkout.html')

