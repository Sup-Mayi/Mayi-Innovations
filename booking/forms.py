from django import forms
from .models import ServiceRequest
from .models import ServiceRequest, ContactMessage

from .models import BuyNewInquiry


class ServiceRequestForm(forms.ModelForm):
    DEVICE_CHOICES = [
        ('laptop', 'Laptop/Desktop'),
        ('mobile', 'Mobile Phone'),
        ('tv', 'Television'),
        ('CCTV', 'CCTV'),
    ]

    device_type = forms.ChoiceField(choices=DEVICE_CHOICES, label="Select Device Type")

    class Meta:
        model = ServiceRequest
        fields = ['device_type','name', 'email', 'phone',  'issue_description', 'state', 'city']
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'phone': forms.TextInput(attrs={'placeholder': '10-digit number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message'}),
        }
# booking/forms.py


from .models import BuyNewInquiry

class BuyNewInquiryForm(forms.ModelForm):
    class Meta:
        model = BuyNewInquiry
        fields = ['name', 'phone', 'email', 'device_type']

    