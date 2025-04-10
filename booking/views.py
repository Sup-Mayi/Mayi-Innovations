from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ServiceRequestForm
from .models import ServiceRequest

def send_whatsapp_message(phone_number, message):
    # For demonstration, you can use the actual WhatsApp API or other third-party APIs
    print(f"Sending message to {phone_number}: {message}")

def index(request):
    return render(request, 'booking/home.html')

def about(request):
    return render(request, 'booking/about.html')

def contact(request):
    return render(request, 'booking/contact.html')

def services(request):
    return render(request, 'booking/services.html')

def success(request):
    return render(request, 'booking/success.html')

def request_service(request):
    print("Requesting service...")  # Add this for debugging
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save()

            # WhatsApp Message
            phone = service_request.phone
            whatsapp_message = f"Thank you for booking with QuickFix! Your ticket ID is {service_request.ticket_id}."
            send_whatsapp_message(phone, whatsapp_message)

            # Email to customer
            send_mail(
                subject='QuickFix - Service Booking Confirmation',
                message=f"""
Hello {service_request.name},

Your service booking was successful!

Ticket ID: {service_request.ticket_id}
Device: {service_request.device_type}
State: {service_request.state}
City: {service_request.city}

Issue: {service_request.issue_description}

We will get in touch with you shortly.

- Team QuickFix
                """,
                from_email='quickfix@example.com',
                recipient_list=[service_request.email],
                fail_silently=False,
            )

            # Email to admin
            send_mail(
                subject='New Service Request - QuickFix',
                message=f"""
A new service request has been submitted!

Ticket ID: {service_request.ticket_id}
Customer Name: {service_request.name}
Device: {service_request.device_type}
State: {service_request.state}
City: {service_request.city}
Phone: {service_request.phone}
Email: {service_request.email}

Issue: {service_request.issue_description}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return render(request, 'booking/success.html', {'ticket_id': service_request.ticket_id})
    else:
        form = ServiceRequestForm()

    return render(request, 'booking/book_now.html', {'form': form})
