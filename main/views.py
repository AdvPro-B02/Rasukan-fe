from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
    }
    resp = render(request, "main.html", context)
    print(request.headers)
    resp["Authorization"] = request.headers.get("Authorization")

    return resp