from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import Company, Customer, User

from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm, ServiceRequestForm


def service_list(request):
    # Get all services ordered by creation date
    services = Service.objects.all().order_by("-created_at")
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    field_filter = request.GET.get('field', '')
    
    # Apply filters if provided
    if search_query:
        services = services.filter(name__icontains=search_query)
    if field_filter:
        services = services.filter(field=field_filter)
    
    # Get unique fields for filter dropdown
    fields = Service.objects.values_list('field', flat=True).distinct()
    
    return render(request, 'services/service_list.html', {
        'services': services,
        'fields': fields,
        'search_query': search_query,
        'field_filter': field_filter
    })


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


@login_required
def create(request):
    # Check if user is a company
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, "Only companies can create services.")
        return redirect('home')

    if request.method == 'POST':
        form = CreateNewService(request.POST)
        if form.is_valid():
            service = Service(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_hour=form.cleaned_data['price_hour'],
                field=form.cleaned_data['field'],
                company=company,
                rating=0  # Set initial rating to 0
            )
            service.save()
            messages.success(request, "Service created successfully!")
            return redirect('service_detail', pk=service.id)
    else:
        form = CreateNewService()

    return render(request, 'services/create.html', {
        'form': form,
        'company_field': company.field,
        'field_choices': Service.FIELD_CHOICES
    })


def service_field(request, field):
    # Convert the field parameter to match the format in the database
    field = field.replace('-', ' ').title()
    
    # Get all services for this field
    services = Service.objects.filter(field=field)
    
    # If no services found, show a message
    if not services.exists():
        messages.info(request, f'No services found in the {field} category.')
        return redirect('service_list')
    
    # Get unique fields for filter dropdown
    fields = Service.objects.values_list('field', flat=True).distinct()
    
    return render(request, 'services/service_list.html', {
        'services': services,
        'fields': fields,
        'field_filter': field,
        'search_query': ''
    })


def request_service(request, id):
    return render(request, 'services/request_service.html', {})


@login_required
def service_detail(request, pk):
    try:
        service = Service.objects.get(pk=pk)
        is_customer = hasattr(request.user, 'customer')
        
        if request.method == 'POST' and is_customer:
            form = ServiceRequestForm(request.POST)
            if form.is_valid():
                service_request = form.save(commit=False)
                service_request.service = service
                service_request.user = request.user
                service_request.total_cost = service.price_hour * service_request.service_time
                service_request.save()
                messages.success(request, 'Service request submitted successfully!')
                return redirect('my_requests')
        else:
            form = ServiceRequestForm()
        
        return render(request, 'services/service_detail.html', {
            'service': service,
            'form': form,
            'is_customer': is_customer
        })
    except Service.DoesNotExist:
        messages.error(request, 'The requested service does not exist.')
        return redirect('service_list')


@login_required
def my_requests(request):
    # Check if user is a customer
    if not hasattr(request.user, 'customer'):
        messages.error(request, "Only customers can view service requests.")
        return redirect('home')
        
    service_requests = ServiceRequest.objects.filter(user=request.user).select_related('service', 'service__company')
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Apply filters if provided
    if search_query:
        service_requests = service_requests.filter(service__name__icontains=search_query)
    if status_filter:
        service_requests = service_requests.filter(status=status_filter)
    
    return render(request, 'services/my_requests.html', {
        'service_requests': service_requests,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': ServiceRequest.STATUS_CHOICES
    })


@login_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    # Check if user is the owner of the service
    if request.user != service.company.user:
        messages.error(request, "You don't have permission to edit this service.")
        return redirect('service_detail', pk=pk)
    
    if request.method == 'POST':
        # Add the field value to the POST data if it's not already there
        post_data = request.POST.copy()
        if 'field' not in post_data:
            post_data['field'] = service.company.field
            
        form = CreateNewService(post_data, choices=[(service.company.field, service.company.field)])
        if form.is_valid():
            service.name = form.cleaned_data['name']
            service.description = form.cleaned_data['description']
            service.price_hour = form.cleaned_data['price_hour']
            service.save()
            messages.success(request, "Service updated successfully!")
            return redirect('service_detail', pk=service.id)
    else:
        form = CreateNewService(
            initial={
                'name': service.name,
                'description': service.description,
                'price_hour': service.price_hour,
                'field': service.field,
            },
            choices=[(service.company.field, service.company.field)]
        )
    
    return render(request, 'services/edit.html', {'form': form, 'service': service})


@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    # Check if user is the owner of the service
    if request.user != service.company.user:
        messages.error(request, "You don't have permission to delete this service.")
        return redirect('service_detail', pk=pk)
    
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service deleted successfully!")
        return redirect('service_list')
    
    return redirect('service_detail', pk=pk)


@login_required
def company_requests(request):
    # Check if user is a company
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, "Only companies can view service requests.")
        return redirect('home')
        
    # Get all service requests for the company's services
    service_requests = ServiceRequest.objects.filter(
        service__company=company
    ).select_related('service', 'user').order_by('-created_at')
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Apply filters if provided
    if search_query:
        service_requests = service_requests.filter(
            service__name__icontains=search_query
        )
    if status_filter:
        service_requests = service_requests.filter(status=status_filter)
    
    return render(request, 'services/company_requests.html', {
        'service_requests': service_requests,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': ServiceRequest.STATUS_CHOICES
    })


@login_required
def update_request_status(request, request_id, new_status):
    try:
        service_request = ServiceRequest.objects.get(id=request_id)
        # Check if the user is the company that owns the service
        if request.user != service_request.service.company.user:
            messages.error(request, "You don't have permission to update this request.")
            return redirect('home')
            
        service_request.status = new_status
        service_request.save()
        messages.success(request, f"Request status updated to {new_status}.")
    except ServiceRequest.DoesNotExist:
        messages.error(request, "Service request not found.")
    
    return redirect('company_requests')
