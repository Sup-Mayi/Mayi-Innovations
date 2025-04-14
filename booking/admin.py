# booking/admin.py

from django.contrib import admin
from .models import ServiceRequest
from .models import ContactMessage
from .models import BuyNewInquiry

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'name', 'email','phone', 'device_type', 'state', 'city', 'issue_description')
    search_fields = ('ticket_id', 'name', 'email','phone')

admin.site.register(ServiceRequest, ServiceRequestAdmin)



class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message')
    search_fields = ('name', 'email', 'phone')

admin.site.register(ContactMessage, ContactMessageAdmin)

class BuyNewInquiryAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'name', 'email', 'phone', 'device_type')
    search_fields = ('ticket_id', 'name', 'email', 'phone')

admin.site.register(BuyNewInquiry, BuyNewInquiryAdmin)



