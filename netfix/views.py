from django.shortcuts import render, get_object_or_404
from django.http import Http404

from users.models import User, Company, Customer
from services.models import Service, ServiceRequest


def home(request):
    return render(request, "users/home.html", {"user": request.user})


def customer_profile(request, name):
    user = get_object_or_404(User, username=name)
    try:
        customer = Customer.objects.get(user=user)
        service_requests = ServiceRequest.objects.filter(user=user)
        return render(
            request,
            "users/customer_profile.html",
            {"customer": customer, "service_requests": service_requests},
        )
    except Customer.DoesNotExist:
        return render(
            request, "users/error.html", {"message": "User is not a customer"}
        )


def company_profile(request, name):
    user = get_object_or_404(User, username=name)
    try:
        company = Company.objects.get(user=user)
        services = Service.objects.filter(company=company).order_by("-created_at")
        return render(
            request,
            "users/company_profile.html",
            {"company": company, "services": services},
        )
    except Company.DoesNotExist:
        return render(request, "users/error.html", {"message": "User is not a company"})


def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "404.html", status=500)
