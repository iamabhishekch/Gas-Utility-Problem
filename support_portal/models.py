from django.db import models
from django.contrib.auth.models import User
from service_requests.models import ServiceRequest

class SupportStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.username} - {self.department}"

class ServiceRequestNote(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='notes')
    staff = models.ForeignKey(SupportStaff, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    internal_only = models.BooleanField(default=False)  # Whether note is visible to customer
    
    def __str__(self):
        return f"Note on {self.service_request.title}"
