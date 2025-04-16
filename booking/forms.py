from django import forms
from .models import ServiceRequest
from .models import ServiceRequest, ContactMessage

from .models import BuyNewInquiry
from django.utils import timezone
from django.core.exceptions import ValidationError
from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()




class ServiceRequestForm(forms.ModelForm):
    DEVICE_CHOICES = [
        ('laptop', 'Laptop/Desktop'),
        ('mobile', 'Mobile Phone'),
        ('tv', 'Tv'),
        ('CCTV', 'CCTV'),
    ]

    device_type = forms.ChoiceField(choices=DEVICE_CHOICES, label="Select Device Type")
    appointment_date = forms.DateTimeField(
        label="Preferred Date & Time", 
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    visit_price = forms.CharField(
        initial="99/-", 
        required=False, 
        label="Visit Price",
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )  
      
    class Meta:
        model = ServiceRequest
        fields = ['device_type', 'name', 'email', 'phone', 'issue_description', 'state', 'city', 'appointment_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now().strftime('%Y-%m-%dT%H:%M')
        self.fields['appointment_date'].widget.attrs['min'] = now    
    def clean_appointment_date(self):
        date = self.cleaned_data.get('appointment_date')
        if date and date < timezone.now():
            raise ValidationError("You cannot select a past date or time.")
        return date   
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
    appointment_date = forms.DateTimeField(
        label="Preferred Appointment Date & Time",
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    # # price = forms.CharField(
    # #     initial="99/-",
    # #     required=False,
    # #     label="Estimated Price",
    # #     widget=forms.TextInput(attrs={'readonly': 'readonly'})
    # )

    class  Meta:
        model = BuyNewInquiry
        fields = ['device_type', 'name', 'email', 'phone', 'state', 'city' ,'appointment_date', 'ticket_id']



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now().strftime('%Y-%m-%dT%H:%M')
        self.fields['appointment_date'].widget.attrs['min'] = now

    def clean_appointment_date(self):
        date = self.cleaned_data.get('appointment_date')
        if date:
        # Make sure both are timezone-aware
            if timezone.is_naive(date):
                date = make_aware(date)
            if date < timezone.now():
                raise ValidationError("You cannot select a past date or time.")
        return date   
