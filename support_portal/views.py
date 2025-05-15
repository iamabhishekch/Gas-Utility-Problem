from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone

from .models import SupportStaff, ServiceRequestNote
from .forms import ServiceRequestNoteForm, AssignServiceRequestForm
from service_requests.models import ServiceRequest

@login_required
def support_dashboard(request):
    try:
        staff = SupportStaff.objects.get(user=request.user)
    except SupportStaff.DoesNotExist:
        # Also allow admin users
        if request.user.is_staff:
            # For admin users who don't have a proper staff profile
            # we'll just create one on the fly for convenience
            staff = SupportStaff.objects.create(
                user=request.user,
                staff_id=f"ADMIN{request.user.id}",
                department="Administration"
            )
            messages.info(request, 'Admin access granted to support portal.')
        else:
            return HttpResponseForbidden("Access restricted to support staff only")
    
    # Get assigned requests for this staff member
    assigned_requests = ServiceRequest.objects.filter(assigned_to=staff)
    
    # Get unassigned requests
    unassigned_requests = ServiceRequest.objects.filter(assigned_to__isnull=True)
    
    return render(request, 'support_portal/dashboard.html', {
        'staff': staff,
        'assigned_requests': assigned_requests,
        'unassigned_requests': unassigned_requests
    })

@login_required
def request_detail(request, pk):
    try:
        staff = SupportStaff.objects.get(user=request.user)
    except SupportStaff.DoesNotExist:
        # Also allow admin users
        if request.user.is_staff:
            # For admin users who don't have a proper staff profile
            # we'll just create one on the fly for convenience
            staff = SupportStaff.objects.create(
                user=request.user,
                staff_id=f"ADMIN{request.user.id}",
                department="Administration"
            )
            messages.info(request, 'Admin access granted to support detail view.')
        else:
            return HttpResponseForbidden("Access restricted to support staff only")
    
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    
    if request.method == 'POST':
        if 'add_note' in request.POST:
            note_form = ServiceRequestNoteForm(request.POST)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.service_request = service_request
                note.staff = staff
                note.save()
                messages.success(request, 'Note added successfully.')
        
        elif 'assign_request' in request.POST:
            assign_form = AssignServiceRequestForm(request.POST, instance=service_request)
            if assign_form.is_valid():
                assign_form.save()
                messages.success(request, 'Request assigned successfully.')
        
        elif 'resolve_request' in request.POST:
            service_request.status = 'COMPLETED'
            service_request.resolved_at = timezone.now()
            service_request.save()
            messages.success(request, 'Request marked as resolved.')
        
        return redirect('support_request_detail', pk=service_request.pk)
    
    note_form = ServiceRequestNoteForm()
    assign_form = AssignServiceRequestForm(instance=service_request)
    
    return render(request, 'support_portal/request_detail.html', {
        'service_request': service_request,
        'note_form': note_form,
        'assign_form': assign_form,
        'staff': staff,
        'notes': service_request.notes.all().order_by('-created_at')
    })
