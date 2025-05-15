from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm
from .models import Customer

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer/register.html', {'form': form})

@login_required
def profile(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, 'Customer profile not found.')
        return redirect('home')
    
    return render(request, 'customer/profile.html', {'customer': customer})

@login_required
def dashboard(request):
    try:
        customer = Customer.objects.get(user=request.user)
        service_requests = customer.service_requests.all().order_by('-created_at')
    except Customer.DoesNotExist:
        messages.error(request, 'Customer profile not found.')
        return redirect('home')
    
    return render(request, 'customer/dashboard.html', {
        'customer': customer,
        'service_requests': service_requests
    })
