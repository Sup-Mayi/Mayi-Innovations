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
import pandas as pd
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import ServiceRequest
import pandas as pd
from django.db import connection

from django.http import HttpResponse
from .models import ServiceRequest  # Replace with your actual model

def gallery(request):
    return render(request, 'booking/gallery.html')



# Function to fetch data from a table and return it as a DataFrame
def fetch_data_from_table(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
    return df

# View to export data to Excel
def export_data(request):
    # Fetch data from each table
    contact_message_df = fetch_data_from_table('booking_contactmessage')
    session_df = fetch_data_from_table('django_session')
    service_request_df = fetch_data_from_table('booking_servicerequest')
    buy_new_inquiry_df = fetch_data_from_table('booking_buynewinquiry')

    if contact_message_df.empty:
        print("No data fetched for 'booking_contactmessage' table.")
    if session_df.empty:
        print("No data fetched for 'django_session' table.")
    if service_request_df.empty:
        print("No data fetched for 'booking_servicerequest' table.")
    if buy_new_inquiry_df.empty:
        print("No data fetched for 'booking_buynewinquiry' table.")

    # Create an HttpResponse to download the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=exported_data.xlsx'

    # Create a writer to write data to the Excel file with multiple sheets
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        contact_message_df.to_excel(writer, sheet_name='ContactMessage', index=False)
        session_df.to_excel(writer, sheet_name='Session', index=False)
        service_request_df.to_excel(writer, sheet_name='ServiceRequest', index=False)
        buy_new_inquiry_df.to_excel(writer, sheet_name='BuyNewInquiry', index=False)

    return response


def import_excel_data(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                # Read the Excel file into a DataFrame
                df = pd.read_excel(excel_file)

                # Iterate over the DataFrame rows and create ServiceRequest objects
                for _, row in df.iterrows():
                    ServiceRequest.objects.create(
                        name=row['name'],
                        email=row['email'],
                        phone=row['phone'],
                        device_type=row['device_type'],
                        state=row['state'],
                        city=row['city'],
                        issue_description=row['issue_description'],
                        ticket_id=row['ticket_id'],
                        # Add other fields as necessary
                    )
                return redirect('success')  # Redirect to a success page
            except Exception as e:
                form.add_error('excel_file', f'Error processing file: {e}')
    else:
        form = ExcelUploadForm()
    return render(request, 'booking/import.html', {'form': form})


def export_service_requests_to_excel(request):
    # Query all ServiceRequest records
    queryset = ServiceRequest.objects.all().values()
    
    # Convert queryset to DataFrame
    df = pd.DataFrame(list(queryset))
    
    # Create an in-memory output file for the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=service_requests.xlsx'
    
    # Use pandas to write the DataFrame to the Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='ServiceRequests')
    
    return response

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



# Function to generate unique ticket ID
def generate_ticket_id():
    while True:
        # Generate a random ticket ID
        ticket_id = 'QFB-' + ''.join(random.choices(string.digits, k=4))
        
        # Check if the ticket ID already exists in the database
        if not BuyNewInquiry.objects.filter(ticket_id=ticket_id).exists():
            return ticket_id
        
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
                message=(
                    f"Hi {inquiry.name},\n\n"
                    f"Thank you for inquiring about a new {inquiry.device_type}.\n"
                    f"Your Ticket ID: {inquiry.ticket_id}\n"
                    f"State: {inquiry.state}\n"
                    f"City: {inquiry.city}\n\n"
                    f"We will get back to you shortly."
                ),
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
State: {inquiry.state}
City: {inquiry.city}
                """,
                from_email='quickfix@example.com',
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return render(request, 'booking/success.html', {'ticket_id': inquiry.ticket_id})
    else:
        form = BuyNewInquiryForm()

    return render(request, 'booking/buy_new_inquiry.html', {'form': form})

