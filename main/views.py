from django.shortcuts import render

# Create your views here.
def show_main(request):
    return render(request, "main.html", {})


def handle_404(request, exception=None):
    return render(request, "404.html", {})
