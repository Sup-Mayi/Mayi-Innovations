from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('book-now/', views.request_service, name='book_now'),
    path('success/', views.success, name='success'),
     path('contact-success/', views.contact_success, name='contact_success'),
     path('book-now/', views.request_service, name='request_service'),
        path('buy-new/', views.buy_new_inquiry, name='buy_new_inquiry'),

]
