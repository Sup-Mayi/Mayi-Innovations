# booking/models.py
from django.db import models
import uuid

class ServiceRequest(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Auto-generate ticket_id
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    device_type = models.CharField(max_length=50)
    issue_description = models.TextField()
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.device_type} issue"
