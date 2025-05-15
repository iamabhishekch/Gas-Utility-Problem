from django import forms
from .models import ServiceRequestNote
from service_requests.models import ServiceRequest

class ServiceRequestNoteForm(forms.ModelForm):
    class Meta:
        model = ServiceRequestNote
        fields = ['content', 'internal_only']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class AssignServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['assigned_to', 'status']
