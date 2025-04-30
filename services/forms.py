from django import forms

from users.models import Company
from .models import Service, ServiceRequest


class CreateNewService(forms.Form):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service name'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter service description'})
    )
    price_hour = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price per hour'})
    )
    field = forms.ChoiceField(
        choices=Service.FIELD_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove 'All in One' from choices if it exists
        self.fields['field'].choices = [
            choice for choice in Service.FIELD_CHOICES 
            if choice[0] != 'All in One'
        ]
        # Make field read-only since it's forced to be the company's field
        self.fields['field'].widget.attrs['readonly'] = True
        self.fields['field'].widget.attrs['disabled'] = True


class RequestServiceForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message to the service provider'})
    )


class ServiceRequestForm(forms.ModelForm):
    service_time = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0.5,
        max_value=24,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter hours needed (0.5-24)',
            'class': 'form-control',
            'step': '0.5'
        }),
        help_text="Enter the number of hours needed for the service (minimum 0.5 hours, maximum 24 hours)"
    )

    class Meta:
        model = ServiceRequest
        fields = ['message', 'address', 'service_time']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your requirements...',
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter the address where the service is required',
                'class': 'form-control'
            }),
        }
        labels = {
            'message': 'Requirements',
            'address': 'Service Address',
            'service_time': 'Hours Needed'
        }
        help_texts = {
            'message': 'Describe what you need help with',
            'address': 'Where should the service be performed?',
        }
