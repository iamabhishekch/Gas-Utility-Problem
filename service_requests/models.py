from django.db import models
from customer.models import Customer
from django.utils import timezone

class ServiceRequestType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='service_requests')
    request_type = models.ForeignKey(ServiceRequestType, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        'support_portal.SupportStaff', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_requests'
    )
    
    def __str__(self):
        return f"{self.title} - {self.customer.user.username} - {self.status}"
    
    def resolve(self):
        self.status = 'COMPLETED'
        self.resolved_at = timezone.now()
        self.save()

class ServiceRequestAttachment(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='request_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attachment for {self.service_request.title}"
