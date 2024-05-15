from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

import requests

# Create your views here.
@csrf_exempt
def register(request):
    context = {}
    
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone_num = request.POST.get("phoneNumber")
        data = {"name": name, "password": password, "email": email, "phoneNumber": phone_num}
        
        r = requests.post("http://localhost:8080/auth/register", data=data)
        if r.status_code == 201:
            return redirect("authentication:login")

    return render(request, "register.html", context)


@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        data = {"email": email, "password": password}
        
        r = requests.post("http://localhost:8080/auth/login", data=data)
        print(r.headers)
        if r.status_code == 200:
            resp = redirect("main:show_main")
            # resp["Authorization"] = r.headers.get("Authorization")
            resp.set_cookie("Authorization", r.headers.get("Authorization"))
            return resp
        else:
            messages.info(
                request,
                "Incorrect email or password"
            )
    
    return render(request, "login.html", {})
