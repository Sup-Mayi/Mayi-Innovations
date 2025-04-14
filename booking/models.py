# booking/models.py
from django.db import models
import uuid
import random
import string

def generate_ticket_id():
    return f"QFB-{random.randint(1000, 9999)}"



class ServiceRequest(models.Model):
    ticket_id = models.CharField(max_length=20, unique=True,blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    device_type = models.CharField(max_length=50)
    issue_description = models.TextField()
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            new_ticket_id = generate_ticket_id()
            # Check uniqueness
            while ServiceRequest.objects.filter(ticket_id=new_ticket_id).exists():
                new_ticket_id = generate_ticket_id()
            self.ticket_id = new_ticket_id
        super().save(*args, **kwargs)
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



class BuyNewInquiry(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket_id} - {self.name}"
    

