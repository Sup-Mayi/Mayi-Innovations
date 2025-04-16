# booking/admin.py

from django.contrib import admin
from .models import ServiceRequest
from .models import ContactMessage
from .models import BuyNewInquiry

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'name', 'email','phone', 'device_type', 'state', 'city', 'issue_description','status')
    search_fields = ('ticket_id', 'name', 'email','phone')
    fields = ('ticket_id', 'name', 'email', 'phone', 'device_type', 'issue_description', 'state', 'city', 'status')
    readonly_fields = ('ticket_id',)

admin.site.register(ServiceRequest, ServiceRequestAdmin)

 

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message')
    search_fields = ('name', 'email', 'phone')

admin.site.register(ContactMessage, ContactMessageAdmin)

class BuyNewInquiryAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'name', 'email', 'phone', 'device_type', 'state', 'city','status')
    search_fields = ('ticket_id', 'name', 'email', 'phone')
    fields = ('ticket_id', 'name', 'email', 'phone', 'device_type', 'appointment_date', 'price', 'status')
    readonly_fields = ('ticket_id',)
admin.site.register(BuyNewInquiry, BuyNewInquiryAdmin)



