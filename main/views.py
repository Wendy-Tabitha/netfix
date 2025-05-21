from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from main.models import HomePage


def home(request):
    try:
        homepage = HomePage.objects.first()
        return render(request, "main/home.html", {"homepage": homepage})
    except:
        return render(request, "main/home.html", {})


def logout(request):
    django_logout(request)
    return redirect("main:home")
