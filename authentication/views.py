from django.http import HttpRequest
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

import requests

# Create your views here.
def register(request: HttpRequest):
    context = {}
    
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone_num = request.POST.get("phoneNumber")
        data = {"name": name, "password": password, "email": email, "phoneNumber": phone_num}
        
        r = requests.post(f"{settings.AUTH_URL}/auth/register", data=data)
        if r.status_code == 201:
            return redirect("authentication:login")

    return render(request, "register.html", context)


def login(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            request.session["id"] = user.id
            request.session["name"] = user.username
            request.session["balance"] = user.balance
            resp = redirect("main:show_main")
            resp.set_cookie("token", request.COOKIES["token"])
            resp.set_cookie("staff", request.COOKIES["staff"])
            return resp
        else:
            messages.info(
                request,
                "Incorrect email or password"
            )
    
    return render(request, "login.html", {})


def logout(request: HttpRequest):
    resp = redirect("main:show_main")
    resp.delete_cookie("token")
    resp.delete_cookie("staff")
    request.session.delete("id")
    request.session.delete("name")
    request.session.delete("balance")
    return resp
