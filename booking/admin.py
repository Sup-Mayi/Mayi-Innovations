# booking/admin.py

from django.contrib import admin
from .models import ServiceRequest

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'name', 'email', 'device_type', 'state', 'city', 'issue_description')
    search_fields = ('ticket_id', 'name', 'email')

admin.site.register(ServiceRequest, ServiceRequestAdmin)
