from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from customer.models import Customer
from .models import ServiceRequest, ServiceRequestType, ServiceRequestAttachment
from .forms import ServiceRequestForm, ServiceRequestAttachmentForm

@login_required
def create_service_request(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect("home")
    
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        attachment_form = ServiceRequestAttachmentForm(request.POST, request.FILES)
        
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = customer
            service_request.save()
            
            if attachment_form.is_valid() and attachment_form.cleaned_data.get("file"):
                attachment = attachment_form.save(commit=False)
                attachment.service_request = service_request
                attachment.save()
            
            messages.success(request, "Service request submitted successfully!")
            return redirect("service_request_detail", pk=service_request.pk)
    else:
        form = ServiceRequestForm()
        attachment_form = ServiceRequestAttachmentForm()
    
    return render(request, "service_requests/create_request.html", {
        "form": form,
        "attachment_form": attachment_form,
        "request_types": ServiceRequestType.objects.all()
    })

@login_required
def service_request_detail(request, pk):
    try:
        customer = Customer.objects.get(user=request.user)
        service_request = ServiceRequest.objects.get(pk=pk, customer=customer)
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect("home")
    except ServiceRequest.DoesNotExist:
        messages.error(request, "Service request not found.")
        return redirect("customer_dashboard")
    
    return render(request, "service_requests/request_detail.html", {
        "service_request": service_request
    })

@login_required
def service_request_list(request):
    try:
        customer = Customer.objects.get(user=request.user)
        service_requests = customer.service_requests.all().order_by("-created_at")
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect("home")
    
    return render(request, "service_requests/request_list.html", {
        "service_requests": service_requests
    })

