import requests

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
def topup_main(request: HttpRequest):    
    return render(request, "topup.html", {})


def get_topup(request: HttpRequest):
    resp = requests.get(f"{settings.LSP_URL}/api/topup/user/{request.session.get('id')}")
    return JsonResponse(resp.json(), safe=False, status=200)


def create_topup(request: HttpRequest):
    if request.method == "POST":
        user = request.session.get("id")
        amount = request.POST.get("amount")
        if not amount.isdigit() or int(amount) < 0 or int(amount) > 2147483647:
            messages.error(request, "Amount has to be a positive number between 1 and 2147483647")
        
        else:
            data = {"user": user, "amount": amount}
            requests.post(f"{settings.LSP_URL}/api/topup", data=data)
            return redirect("topup:topup_main")

    return render(request, "create_topup.html", {})


def delete_topup(request: HttpRequest, id: str):
    requests.delete(f"{settings.LSP_URL}/api/topup/{id}")
    return get_topup(request)


def delete_all_topup(request: HttpRequest):
    requests.delete(f"{settings.LSP_URL}/api/topup/user/{request.session.get('id')}")
    return JsonResponse(status=200)
