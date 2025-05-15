from django import forms
from .models import ServiceRequest, ServiceRequestAttachment

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['request_type', 'title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ServiceRequestAttachmentForm(forms.ModelForm):
    class Meta:
        model = ServiceRequestAttachment
        fields = ['file']
