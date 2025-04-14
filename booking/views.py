from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ServiceRequestForm
from .models import ServiceRequest
from .forms import ContactForm
from .models import ContactMessage
import random
import string
from .forms import BuyNewInquiryForm
from .models import BuyNewInquiry

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


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Send confirmation email
            send_mail(
                subject="QuickFix - Thanks for Contacting Us!",
                message=f"Hi {contact_message.name},\n\nThanks for reaching out. We'll get back to you shortly.\n\nYour Message:\n{contact_message.message}",
                from_email='quickfix@example.com',
                recipient_list=[contact_message.email],
                fail_silently=False,
            )
            send_mail(
                subject=f"New Contact Message from {contact_message.name}",
                message=f"""
                Name: {contact_message.name}
                Email: {contact_message.email}
                Phone: {contact_message.phone}
                Message: {contact_message.message}
                    """,
                    from_email='quickfix@example.com',
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
   

            ) 
            

            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'booking/contact.html', {'form': form})
def contact_success(request):
    return render(request, 'booking/contact_success.html')



def generate_ticket_id():
    return 'QFB-' + ''.join(random.choices(string.digits, k=4))

def buy_new_inquiry(request):
    if request.method == 'POST':
        form = BuyNewInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.ticket_id = generate_ticket_id()
            inquiry.save()

            # Send Email to Customer
            send_mail(
                subject="QuickFix - New Device Inquiry Confirmation",
                message=f"Hi {inquiry.name},\n\nThank you for inquiring about a new {inquiry.device_type}.\nYour Ticket ID: {inquiry.ticket_id}\nWe will get back to you shortly.",
                from_email='quickfix@example.com',
                recipient_list=[inquiry.email],
                fail_silently=False,
            )

            # Send Email to Admin
            send_mail(
                subject="New Device Inquiry Submitted",
                message=f"""
New inquiry received:

Ticket ID: {inquiry.ticket_id}
Name: {inquiry.name}
Phone: {inquiry.phone}
Email: {inquiry.email}
Device Type: {inquiry.device_type}
                """,
                from_email='quickfix@example.com',
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return render(request, 'booking/success.html', {'ticket_id': inquiry.ticket_id})
    else:
        form = BuyNewInquiryForm()

    return render(request, 'booking/buy_new_inquiry.html', {'form': form})
