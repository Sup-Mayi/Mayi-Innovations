# booking/models.py
from django.db import models
from django.core.mail import send_mail
from django.conf import settings


import uuid
import random
import string

def generate_ticket_id():
    return f"QFB-{random.randint(1000, 9999)}"



class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('opened', 'Opened'),
        ('progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    ticket_id = models.CharField(max_length=20, unique=True,blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    device_type = models.CharField(max_length=50)
    issue_description = models.TextField()
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='opened')


    def save(self, *args, **kwargs):
        if not self.ticket_id:
            new_ticket_id = generate_ticket_id()
            # Check uniqueness
            while ServiceRequest.objects.filter(ticket_id=new_ticket_id).exists():
                new_ticket_id = generate_ticket_id()
            self.ticket_id = new_ticket_id
        if self.pk:  # Check if object exists and is being updated
            original = ServiceRequest.objects.get(pk=self.pk)
            if original.status != self.status:  # Check if status changed
                self.send_status_email(original.status)
    
        super().save(*args, **kwargs)
    def send_status_email(self, old_status):
        subject = f"Ticket {self.ticket_id} Status Changed"
        message = f"Dear {self.name},\n\nYour ticket (ID: {self.ticket_id}) status has changed.\n\n"
        message += f"Old Status: {old_status.capitalize()}\nNew Status: {self.status.capitalize()}\n\n"
        message += f"Device Type: {self.device_type}\nIssue Description: {self.issue_description}\n"
        message += f"Phone: {self.phone}\nEmail: {self.email}\n\n"
        message += f"State: {self.state}\nCity: {self.city}\n\nThank you for contacting us!"

        # Send email to the user
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )

        # Send email to the admin
        admin_email = 'admin-email@example.com'  # Replace with actual admin email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            fail_silently=False,
        )

    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.device_type} issue"    
   
from django.db import models

class ContactMessage(models.Model):
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

   
    def __str__(self):
        return f"Message from {self.name}"
# booking/models.py


from django.utils import timezone
class BuyNewInquiry(models.Model):
    STATUS_CHOICES = [
        ('opened', 'Opened'),
        ('progress', 'In Progress'),
        ('closed', 'Closed'),
        
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='opened')
    DEVICE_CHOICES = [
        ('Laptop/Desktop', 'Laptop/Desktop'),
        ('TV', 'TV'),
        ('Mobile', 'Mobile'),
        ('CCTV', 'CCTV'),

    ]

    ticket_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    device_type = models.CharField(max_length=20, choices=DEVICE_CHOICES)
    
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    appointment_date = models.DateTimeField()

    price = models.CharField(max_length=10, default='TBD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='opened')



    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:  # Check if object exists and is being updated
            original = BuyNewInquiry.objects.get(pk=self.pk)
            if original.status != self.status:  # Check if status changed
                self.send_status_email(original.status)

        super().save(*args, **kwargs)

    def send_status_email(self, old_status):
        subject = f"Inquiry {self.ticket_id} Status Changed"
        message = f"Dear {self.name},\n\nYour inquiry (ID: {self.ticket_id}) status has changed.\n\n"
        message += f"Old Status: {old_status.capitalize()}\nNew Status: {self.status.capitalize()}\n\n"
        # message += f"Device Type: {self.device_type}\nState: {self.state}\nCity: {self.city}\n"
        message += f"Phone: {self.phone}\nEmail: {self.email}\n\n"
        message += f"Device Type: {self.device_type}\n"
        message += f"Appointment Date: {self.appointment_date}\n\nThank you for contacting us!"

        # Send email to the user
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )

        # Send email to the admin
        admin_email = 'admin-email@example.com'  # Replace with actual admin email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            fail_silently=False,
        )

    def __str__(self):
        return f"{self.ticket_id} - {self.name}"

