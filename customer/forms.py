from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                address=self.cleaned_data.get('address'),
                phone_number=self.cleaned_data.get('phone_number'),
                # Generate a simple account number (in a real system, this would be more sophisticated)
                account_number=f"GAS{user.id:06d}"
            )
        return user
