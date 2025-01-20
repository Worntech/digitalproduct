from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User, auth
from . models import *
from . forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView

from django.conf import settings

#changing password
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.core.mail import send_mail

from pesapal.views import *

# FOR PAYMENT
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView

from django_pesapal.views import PaymentRequestMixin

from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Payment, Websitetemplate
from decimal import Decimal
from django.db import transaction

from django.utils.cache import add_never_cache_headers
from django.db.models import Sum
from django.http import JsonResponse

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import time
from django.utils import timezone
from .models import Notification

from .tasks import delete_viewed_notifications
from django.http import JsonResponse

from django.db.models import Q

import random
from itertools import chain
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache

from web.middleware import disable_browser_cache
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db.models import Avg, Count
from math import floor

from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)



# Create your views here.
# @login_required(login_url='signin')
def admin(request):
    return render(request, 'web/admin.html')
def signup(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if MyUser.objects.filter(email=email).exists():
                messages.info(request, f"Email {email} Already Taken")
                return redirect('signup')
            elif MyUser.objects.filter(username=username).exists():
                messages.info(request, f"Username {username} Already Taken")
                return redirect('signup')
            else:
                user = MyUser.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
                user.save()
                # messages.info(request, 'Registered succesefull.')
                
                
                # EMAILING
                subject = "WORNTECH ONLINE SERVICES"
                message = f"Hellow {first_name} {last_name} You have created account in Worntech, welcome and enjoy the service of selling and buyying digital product, if there is any problem contact us. Your user name is: {email} and your password is: {password}, welcome and enjoy the service with worntech online services"
                #from_email = settings.EMAIL_HOST_USER
                from_email = 'worntechservices@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=True)
                return redirect('signupsucces')
        else:
            messages.info(request, 'The Two Passwords Not Matching')
            return redirect('signup')

    else:
        return render(request, 'web/signup.html')

def signin(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.info(request, 'Loged in succesefull.')
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('signin')

    else:
        return render(request, 'web/signin.html')

def logout(request):
    auth.logout(request)
    # messages.info(request, 'Loged out succesefull.')
    return redirect('logedout')

@login_required(login_url='signin')
def change_password(request):
    if request.method == 'POST':
        passwordchange = PasswordChangeForm(request.user, request.POST)
        if passwordchange.is_valid():
            user = passwordchange.save()
            
            # Create a notification for the user
            message = "You have changed your password in worntech online srvices, welcome and enjoy selling and buying digital product."

            # Assuming the user is the one making the request
            Notification.objects.create(
                user=request.user,  # Replace with appropriate user if needed
                message=message,
                status="None"
            )
            
            
            subject = "WORNTECH ONLINE SERVICES"
            message = f"Hellow {request.user.first_name} {request.user.last_name} You have changed your password in worntech online services, if not you please contact us through whatsapp +255 710 891 288"
            #from_email = settings.EMAIL_HOST_USER
            from_email = 'worntechservices@gmail.com'
            recipient_list = [user.request.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
                
            # This is to keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('signin')  # Redirect to the same page after successful password change
        else:
            messages.error(request, 'Please inseart correct information.')
    else:
        passwordchange = PasswordChangeForm(request.user)
    return render(request, 'web/change_password.html', {'passwordchange': passwordchange})

# Custom Password Reset View
class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

# Custom Password Reset Done View
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

# Custom Password Reset Confirm View
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

# Custom Password Reset Complete View
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

def home(request):
    image_count = Image.objects.all().count()
    project_count = Project.objects.all().count()
    
    course_website = Website.objects.all().count()
    course_mobile = Mobile.objects.all().count()
    course_desktop = Desktop.objects.all().count()
    course_embeded = Embeded.objects.all().count()
    course_graphics = Graphics.objects.all().count()
    
    course_websitetemplate = Websitetemplate.objects.all().count()
    course_mobiletemplate = Mobiletemplate.objects.all().count()
    course_desktoptemplate = Desktoptemplate.objects.all().count()
    course_microsofttemplate = Microsofttemplate.objects.all().count()
    course_adobetemplate = Adobetemplate.objects.all().count()
    
    bookcount = Book.objects.all().count()
    printablecount = Printable.objects.all().count()
    musiccount = Music.objects.all().count()
    multmediacount = Multimedia.objects.all().count()
    digitalArtcount = DigitalArt.objects.all().count()
    cadcount = CAD.objects.all().count()
    softwarecount = Software.objects.all().count()
    businesscount = Business.objects.all().count()
    
    course_count = course_website + course_mobile + course_desktop + course_embeded + course_graphics
    template_count = course_websitetemplate + course_mobiletemplate + course_desktoptemplate + course_microsofttemplate + course_adobetemplate
    digital_product_count = bookcount + printablecount + musiccount + multmediacount + cadcount + digitalArtcount + softwarecount + businesscount
    
    context = {
        'template_count': template_count,
        'image_count': image_count,
        'digital_product_count': digital_product_count,
        'project_count': project_count,
    }
    return render(request, 'web/home.html',context)

def aboutus(request):
    return render(request, 'web/aboutus.html')
def base1(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.all().order_by('-id')
    
    # Count the notifications for the logged-in user
    notificationcount = Notification.objects.filter(user=request.user).count()
    
    context = {
        'notification': notification,
        'notificationcount': notificationcount,
    }
    return render(request, 'web/base1.html', context)
def base(request):
    return render(request, 'web/base.html')
def contactus(request):
    contact = Contact.objects.all()
    
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    context={
        "contact":contact,
        "notification":notification,
        "notificationcount":notificationcount,
    }
    return render(request, 'web/contactus.html',context)

def contactpost(request):
    if request.method == "POST":
        contactpost = ContactForm(request.POST)
        if contactpost.is_valid():
            contactpost.save()

            subject = "WORNTECH ONLINE SERVICES"
            message = f"Hellow {request.user.first_name} {request.user.last_name} Thanks for contacting us, worntech online service is working for your message, opinion and question, get read we are here for your, for more infomation contact via whatsapp +255 710 891 288"
            #from_email = settings.EMAIL_HOST_USER
            from_email = 'worntechservices@gmail.com'
            recipient_list = [request.user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            messages.success(request, 'Message sent successfully.')
            return redirect('contactpost')  # Ensure this URL exists in your project
    else:
        contactpost = ContactForm()
    
    context = {
        "contactpost": contactpost
    }
    return render(request, 'web/contactpost.html', context)

def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('EMAIL')
        if email:
            # Check if the email is already subscribed
            if Subscription.objects.filter(email=email).exists():
                messages.error(request, 'This email is already subscribed.')
            else:
                Subscription.objects.create(email=email)  # Save the new subscription
                
                subject = "WORNTECH ONLINE SERVICES"
                message = f"Thanks for subscribing in worntech online services, sell and buy digital product online with worntech online service, welcome and enjoy the services"
                #from_email = settings.EMAIL_HOST_USER
                from_email = 'worntechservices@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=True)
                
                messages.success(request, 'Thank you for subscribing!')

        return redirect('successsubscription')  # Change to the appropriate template name or URL

    return render(request, 'web/successsubscription.html')  # Change to your template


@login_required(login_url='signin')
def contactlist(request):
    contactlist = Contact.objects.all()
    countmessage= Contact.objects.all().count()
    context={
        "contactlist":contactlist,
        "countmessage":countmessage
    }
    return render(request, 'web/contactlist.html', context)
@login_required(login_url='signin')
def viewcontact(request, id):
    contact = Contact.objects.get(id=id)
    
    context = {"contact":contact}
    return render(request, 'web/viewcontact.html', context)
@login_required(login_url='signin')
def deletecontact(request, id):
    contact = Contact.objects.get(id=id)
    if request.method == "POST":
        contact.delete()
        messages.info(request, 'Message deleted succesefull.')
        return redirect('contactlist')
    
    context = {"contact":contact}
    return render(request, 'web/deletecontact.html', context)


@login_required(login_url='signin')
def dashboard(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    # Try to get the Myamount record for the user; if it doesn't exist, create a default one
    my_amount_record = Myamount.objects.filter(user=request.user).first()
    
    if not my_amount_record:
        # If the record does not exist, create a default one with 0.00 values
        my_amount_record = {
            'Total_amount': Decimal('0.00'),
            'My_amount': Decimal('0.00'),
            'Reducted_amount': Decimal('0.00'),
            'Withdrawed_amount': Decimal('0.00'),
        }
    else:
        my_amount_record = {
            'Total_amount': my_amount_record.Total_amount,
            'My_amount': my_amount_record.My_amount,
            'Reducted_amount': my_amount_record.Reducted_amount,
            'Withdrawed_amount': my_amount_record.Withdrawed_amount,
        }

    # Count the images, projects, and various courses/templates
    image_count = Image.objects.filter(user=request.user).count()
    project_count = Project.objects.filter(user=request.user).count()

    course_website = Website.objects.filter(user=request.user).count()
    course_mobile = Mobile.objects.filter(user=request.user).count()
    course_desktop = Desktop.objects.filter(user=request.user).count()
    course_embeded = Embeded.objects.filter(user=request.user).count()
    course_graphics = Graphics.objects.filter(user=request.user).count()

    course_websitetemplate = Websitetemplate.objects.filter(user=request.user).count()
    course_mobiletemplate = Mobiletemplate.objects.filter(user=request.user).count()
    course_desktoptemplate = Desktoptemplate.objects.filter(user=request.user).count()
    course_microsofttemplate = Microsofttemplate.objects.filter(user=request.user).count()
    course_adobetemplate = Adobetemplate.objects.filter(user=request.user).count()
    
    bookcount = Book.objects.filter(user=request.user).count()
    printablecount = Printable.objects.filter(user=request.user).count()
    musiccount = Music.objects.filter(user=request.user).count()
    multmediacount = Multimedia.objects.filter(user=request.user).count()
    digitalArtcount = DigitalArt.objects.filter(user=request.user).count()
    cadcount = CAD.objects.filter(user=request.user).count()
    softwarecount = Software.objects.filter(user=request.user).count()
    businesscount = Business.objects.filter(user=request.user).count()

    course_count = course_website + course_mobile + course_desktop + course_embeded + course_graphics
    template_count = course_websitetemplate + course_mobiletemplate + course_desktoptemplate + course_microsofttemplate + course_adobetemplate

    context = {
        'my_amount_record': my_amount_record,
        'image_count': image_count,
        'project_count': project_count,
        'course_count': course_count,
        'template_count': template_count,
        
        'bookcount': bookcount,
        'printablecount': printablecount,
        'musiccount': musiccount,
        'multmediacount': multmediacount,
        'digitalArtcount': digitalArtcount,
        'cadcount': cadcount,
        'softwarecount': softwarecount,
        'businesscount': businesscount,
        
        'notification': notification,
        'notificationcount': notificationcount,
    }
    
    return render(request, 'web/dashboard.html', context)

@login_required(login_url='signin')
def masterdashboard(request):
    user_amount = Myamount.objects.aggregate(total=Sum('My_amount'))['total']
    masteramount = get_object_or_404(MasterAmount, unique_code='welcomemasterofus')
    allusers = MyUser.objects.all().count()
    adminusers = MyUser.objects.filter(is_admin=True).count()
    staffusers = MyUser.objects.filter(is_staff=True).count()
    superuserusers = MyUser.objects.filter(is_superuser=True).count()
    image_count = Image.objects.all().count()
    project_count = Project.objects.all().count()
    
    course_website = Website.objects.all().count()
    course_mobile = Mobile.objects.all().count()
    course_desktop = Desktop.objects.all().count()
    course_embeded = Embeded.objects.all().count()
    course_graphics = Graphics.objects.all().count()
    
    course_websitetemplate = Websitetemplate.objects.all().count()
    course_mobiletemplate = Mobiletemplate.objects.all().count()
    course_desktoptemplate = Desktoptemplate.objects.all().count()
    course_microsofttemplate = Microsofttemplate.objects.all().count()
    course_adobetemplate = Adobetemplate.objects.all().count()
    
    bookcount = Book.objects.all().count()
    printablecount = Printable.objects.all().count()
    musiccount = Music.objects.all().count()
    multmediacount = Multimedia.objects.all().count()
    digitalArtcount = DigitalArt.objects.all().count()
    cadcount = CAD.objects.all().count()
    softwarecount = Software.objects.all().count()
    businesscount = Business.objects.all().count()
    
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    course_count = course_website + course_mobile + course_desktop + course_embeded + course_graphics
    template_count = course_websitetemplate + course_mobiletemplate + course_desktoptemplate + course_microsofttemplate + course_adobetemplate
    
    if user_amount is None:
        user_amount = Decimal('0.00')
    else:
        user_amount = round(user_amount, 2)
        
    total_amount = user_amount + masteramount.My_amount + masteramount.Gateway_Amount

    context = {
        'total_amount': total_amount,
        'user_amount': user_amount,
        'masteramount': masteramount,
        'image_count': image_count,
        'project_count': project_count,
        'course_count': course_count,
        'template_count': template_count,
        'allusers': allusers,
        'adminusers': adminusers,
        'staffusers': staffusers,
        'superuserusers': superuserusers,
        
        'bookcount': bookcount,
        'printablecount': printablecount,
        'musiccount': musiccount,
        'multmediacount': multmediacount,
        'digitalArtcount': digitalArtcount,
        'cadcount': cadcount,
        'softwarecount': softwarecount,
        'businesscount': businesscount,
        
        'notification': notification,
        'notificationcount': notificationcount,
    }
    return render(request, 'web/masterdashboard.html', context)

def services(request):
    return render(request, 'web/services.html')

# courses to be tought
# @login_required(login_url='signin')
def computercs(request):
    return render(request, 'web/computercs.html')
# @login_required(login_url='signin')
def computereng(request):
    return render(request, 'web/computereng.html')
# @login_required(login_url='signin')
def electrical(request):
    return render(request, 'web/electrical.html')
# @login_required(login_url='signin')
def civil(request):
    return render(request, 'web/civil.html')
# @login_required(login_url='signin')
def mechanical(request):
    return render(request, 'web/mechanical.html')
# @login_required(login_url='signin')
def artificial(request):
    return render(request, 'web/artificial.html')
# @login_required(login_url='signin')
def softwareeng(request):
    return render(request, 'web/softwareeng.html')
# @login_required(login_url='signin')
def embeded(request):
    return render(request, 'web/embeded.html')
# @login_required(login_url='signin')
def website(request):
    return render(request, 'web/website.html')
# @login_required(login_url='signin')
def mobileapp(request):
    return render(request, 'web/mobileapp.html')
# @login_required(login_url='signin')
def virtualreality(request):
    return render(request, 'web/virtualreality.html')
# @login_required(login_url='signin')
def security(request):
    return render(request, 'web/security.html')
# @login_required(login_url='signin')
def desktopapp(request):
    return render(request, 'web/desktopapp.html')
# @login_required(login_url='signin')
def multmedia(request):
    return render(request, 'web/multmedia.html')
# @login_required(login_url='signin')
def graphics(request):
    return render(request, 'web/graphics.html')
# @login_required(login_url='signin')
def iot(request):
    return render(request, 'web/iot.html')
# @login_required(login_url='signin')
def security(request):
    return render(request, 'web/security.html')
# @login_required(login_url='signin')
def nertworking(request):
    return render(request, 'web/nertworking.html')

# views for success message
def signupsucces(request):
    return render(request, 'web/signupsucces.html')
def logedout(request):
    return render(request, 'web/logedout.html')

# for website frontend development
# @login_required(login_url='signin')
def wfrontend(request):
    return render(request, 'web/wfrontend.html')

# @login_required(login_url='signin')
def htmlcss(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/htmlcss.html',context)

# @login_required(login_url='signin')
def javascript(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/javascript.html',context)

# @login_required(login_url='signin')
def reactjs(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/reactjs.html',context)

# @login_required(login_url='signin')
def vuejs(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/vuejs.html',context)

# @login_required(login_url='signin')
def bootstrap(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/bootstrap.html',context)

# @login_required(login_url='signin')
def angularjs(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/angularjs.html',context)

# for website backend development
# @login_required(login_url='signin')
def wbackend(request):
    return render(request, 'web/wbackend.html')

# @login_required(login_url='signin')
def django(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/django.html',context)

# @login_required(login_url='signin')
def flask(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/flask.html',context)

# @login_required(login_url='signin')
def php(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/php.html',context)

# @login_required(login_url='signin')
def laravel(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/laravel.html',context)

# @login_required(login_url='signin')
def rub(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/rub.html',context)

# for full stack website development
# @login_required(login_url='signin')
def wfullstack(request):
    return render(request, 'web/wfullstack.html')

# @login_required(login_url='signin')
def djangohtml(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/djangohtml.html',context)

# @login_required(login_url='signin')
def flaskhtml(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/flaskhtml.html',context)

# @login_required(login_url='signin')
def phphtml(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/phphtml.html',context)

# @login_required(login_url='signin')
def laravelhtml(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/laravelhtml.html',context)

# @login_required(login_url='signin')
def djangoreact(request):
    website = Website.objects.all()
    context={
        "website":website
    }
    return render(request, 'web/djangoreact.html',context)

# for mobile application frontend
# @login_required(login_url='signin')
def mfrontend(request):
    return render(request, 'web/mfrontend.html')

# @login_required(login_url='signin')
def reactnative(request):
    mobile = Mobile.objects.all()
    context={
        "mobile":mobile
    }
    return render(request, 'web/reactnative.html',context)

# @login_required(login_url='signin')
def kivy(request):
    mobile = Mobile.objects.all()
    context={
        "mobile":mobile
    }
    return render(request, 'web/kivy.html',context)
# @login_required(login_url='signin')
def fluter(request):
    mobile = Mobile.objects.all()
    context={
        "mobile":mobile
    }
    return render(request, 'web/fluter.html',context)

#for mobile application backnd development
# @login_required(login_url='signin')
def mbackend(request):
    return render(request, 'web/mbackend.html')

# @login_required(login_url='signin')
def mdjango(request):
    mobile = Mobile.objects.all()
    context={
        "mobile":mobile
    }
    return render(request, 'web/django.html',context)

# @login_required(login_url='signin')
def mflask(request):
    mobile = Mobile.objects.all()
    context={
        "mobile":mobile
    }
    return render(request, 'web/flask.html',context)

# @login_required(login_url='signin')
def mfirebase(request):
    mobile = Mobile.objects.all()
    context={
        "mobile":mobile
    }
    return render(request, 'web/firebase.html',context)

#for mobile application full stack development
# @login_required(login_url='signin')
def mfullstack(request):
    return render(request, 'web/mfullstack.html')

# @login_required(login_url='signin')
def reactnativedjango(request):
    mobile = Mobile.objects.all()
    context={
        "mobile":mobile
    }
    return render(request, 'web/reactnativedjango.html',context)

# @login_required(login_url='signin')
def reactnativeflask(request):
    mobile = Mobile.objects.all()
    context={
        "mobile":mobile
    }
    return render(request, 'web/reactnativeflask.html',context)

# @login_required(login_url='signin')
def reactnativefirebase(request):
    mobile = Mobile.objects.all()
    context={
        "mobile":mobile
    }
    return render(request, 'web/reactnativefirebase.html',context)

# for desktop application
# @login_required(login_url='signin')
def cdeskapp(request):
    desktop = Desktop.objects.all()
    context={
        "desktop":desktop
    }
    return render(request, 'web/cdeskapp.html',context)
# @login_required(login_url='signin')
def pdeskapp(request):
    desktop = Desktop.objects.all()
    context={
        "desktop":desktop
    }
    return render(request, 'web/pdeskapp.html',context)

# @login_required(login_url='signin')
def kdeskapp(request):
    desktop = Desktop.objects.all()
    context={
        "desktop":desktop
    }
    return render(request, 'web/kdeskapp.html',context)

# for embeded system
# @login_required(login_url='signin')
def cembeded(request):
    embeded = Embeded.objects.all()
    context={
        "embeded":embeded
    }
    return render(request, 'web/cembeded.html',context)
# @login_required(login_url='signin')
def aembeded(request):
    embeded = Embeded.objects.all()
    context={
        "embeded":embeded
    }
    return render(request, 'web/aembeded.html',context)

# @login_required(login_url='signin')
def pembeded(request):
    embeded = Embeded.objects.all()
    context={
        "embeded":embeded
    }
    return render(request, 'web/pembeded.html',context)

# @login_required(login_url='signin')
def mpembeded(request):
    embeded = Embeded.objects.all()
    context={
        "embeded":embeded
    }
    return render(request, 'web/mpembeded.html',context)

# for graphics designing
# @login_required(login_url='signin')
def photoshop(request):
    graphics = Graphics.objects.all()
    context={
        "graphics":graphics
    }
    return render(request, 'web/photoshop.html',context)

# @login_required(login_url='signin')
def illustrator(request):
    graphics = Graphics.objects.all()
    context={
        "graphics":graphics
    }
    return render(request, 'web/illustrator.html',context)


# FOR PROJECT
# @login_required(login_url='signin')
def websiteproject(request):
    project = Project.objects.order_by('?')
    
    # Prepare data for each template
    for template in project:
        avg_rating = ReviewProject.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewProject.objects.filter(template=template).count()  # Total reviews
        
    context={
        "project":project
    }
    return render(request, 'web/websiteproject.html',context)

# @login_required(login_url='signin')
def mobileproject(request):
    project = Project.objects.order_by('?')
    
    # Prepare data for each template
    for template in project:
        avg_rating = ReviewProject.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewProject.objects.filter(template=template).count()  # Total reviews
        
    context={
        "project":project
    }
    return render(request, 'web/mobileproject.html',context)

# @login_required(login_url='signin')
def desktopproject(request):
    project = Project.objects.order_by('?')
    
    # Prepare data for each template
    for template in project:
        avg_rating = ReviewProject.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewProject.objects.filter(template=template).count()  # Total reviews
        
    context={
        "project":project
    }
    return render(request, 'web/desktopproject.html',context)

# @login_required(login_url='signin')
def artificialproject(request):
    project = Project.objects.order_by('?')
    
    # Prepare data for each template
    for template in project:
        avg_rating = ReviewProject.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewProject.objects.filter(template=template).count()  # Total reviews
        
    context={
        "project":project
    }
    return render(request, 'web/artificialproject.html',context)

# @login_required(login_url='signin')
def embededproject(request):
    project = Project.objects.order_by('?')
    
    # Prepare data for each template
    for template in project:
        avg_rating = ReviewProject.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewProject.objects.filter(template=template).count()  # Total reviews
        
    context={
        "project":project
    }
    return render(request, 'web/embededproject.html',context)

# @login_required(login_url='signin')
def iotproject(request):
    project = Project.objects.order_by('?')
    
    # Prepare data for each template
    for template in project:
        avg_rating = ReviewProject.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewProject.objects.filter(template=template).count()  # Total reviews
        
    context={
        "project":project
    }
    return render(request, 'web/iotproject.html',context)

# @login_required(login_url='signin')
def virtualrealityproject(request):
    project = Project.objects.order_by('?')
    
    # Prepare data for each template
    for template in project:
        avg_rating = ReviewProject.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewProject.objects.filter(template=template).count()  # Total reviews
        
    context={
        "project":project
    }
    return render(request, 'web/virtualrealityproject.html',context)

# @login_required(login_url='signin')
def cyberproject(request):
    project = Project.objects.order_by('?')
    
    # Prepare data for each template
    for template in project:
        avg_rating = ReviewProject.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewProject.objects.filter(template=template).count()  # Total reviews
        
    context={
        "project":project
    }
    return render(request, 'web/cyberproject.html',context)

# @login_required(login_url='signin')
def image(request):
    image = Image.objects.order_by('?')
    
    # Prepare data for each template
    for template in image:
        avg_rating = ReviewImage.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewImage.objects.filter(template=template).count()  # Total reviews
        
    context={
        "image":image
    }
    return render(request, 'web/image.html',context)

# template download
# @login_required(login_url='signin')
def webtemplate(request):
    return render(request, 'web/webtemplate.html')

# @login_required(login_url='signin')
def htmlcsstemplate(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate,
    }
    return render(request, 'web/htmlcsstemplate.html',context)

# @login_required(login_url='signin')
def reacttemplate(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/reacttemplate.html',context)

def vueJs_template(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/vueJs_template.html',context)

def elm(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/elm.html',context)

def swift(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/swift.html',context)

def JQuery(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/JQuery.html',context)

def flutter_template(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/flutter_template.html',context)

def svelte(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/svelte.html',context)

def materialize_CSS(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/materialize_CSS.html',context)

def foundation(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/foundation.html',context)

def angular_template(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/angular_template.html',context)

def tailwind_CSS(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/tailwind_CSS.html',context)

def bootstrap_template(request):
    websitetemplate = Websitetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in websitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "websitetemplate":websitetemplate
    }
    return render(request, 'web/bootstrap_template.html',context)


# @login_required(login_url='signin')
def mobiletemplate(request):
    return render(request, 'web/mobiletemplate.html')

# @login_required(login_url='signin')
def reactnativetemplate(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/reactnativetemplate.html',context)

def flutter_mobile_template(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/flutter_mobile_template.html',context)

def swiftUI(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/swiftUI.html',context)

def jetpack_Compose(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/jetpack_Compose.html',context)

def ionic_Framework(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/ionic_Framework.html',context)

def xamarin(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/xamarin.html',context)

def phoneGap(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/phoneGap.html',context)

def nativeScript(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/nativeScript.html',context)

def framework_seven(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/framework_seven.html',context)

def onsen_UI(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/onsen_UI.html',context)

def jQuery_Mobile(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/jQuery_Mobile.html',context)

def sencha_Touch(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/sencha_Touch.html',context)

def Kivy_template(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/Kivy_template.html',context)

def bootstrap_Mobile_Templates(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/bootstrap_Mobile_Templates.html',context)

def quasar_Framework(request):
    mobiletemplate = Mobiletemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in mobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "mobiletemplate":mobiletemplate
    }
    return render(request, 'web/quasar_Framework.html',context)


# @login_required(login_url='signin')
def desktoptemplate(request):
    return render(request, 'web/desktoptemplate.html')

# @login_required(login_url='signin')
def kivytemplate(request):
    desktoptemplate = Desktoptemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in desktoptemplate:
        avg_rating = ReviewDesktoptemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDesktoptemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "desktoptemplate":desktoptemplate
    }
    return render(request, 'web/kivytemplate.html',context)

# @login_required(login_url='signin')
def pyqttemplate(request):
    desktoptemplate = Desktoptemplate.objects.order_by('?')
    # Prepare data for each template
    for template in desktoptemplate:
        avg_rating = ReviewDesktoptemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDesktoptemplate.objects.filter(template=template).count()  # Total reviews
        
    desktoptemplate = Desktoptemplate.objects.order_by('?')

    context={
        "desktoptemplate":desktoptemplate
    }
    return render(request, 'web/pyqttemplate.html',context)

# @login_required(login_url='signin')
def ctemplate(request):
    desktoptemplate = Desktoptemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in desktoptemplate:
        avg_rating = ReviewDesktoptemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDesktoptemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "desktoptemplate":desktoptemplate
    }
    return render(request, 'web/ctemplate.html',context)

# @login_required(login_url='signin')
def tkintertemplate(request):
    desktoptemplate = Desktoptemplate.objects.order_by('?')
    
    for template in desktoptemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "desktoptemplate":desktoptemplate
    }
    return render(request, 'web/tkintertemplate.html',context)

# second now continue
def chashdesktopapp(request):
    desktoptemplate = Desktoptemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in desktoptemplate:
        avg_rating = ReviewDesktoptemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDesktoptemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "desktoptemplate":desktoptemplate
    }
    return render(request, 'web/chashdesktopapp.html',context)

def javadesktopapp(request):
    desktoptemplate = Desktoptemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in desktoptemplate:
        avg_rating = ReviewDesktoptemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDesktoptemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "desktoptemplate":desktoptemplate
    }
    return render(request, 'web/javadesktopapp.html',context)

def cplusdesktopapp(request):
    desktoptemplate = Desktoptemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in desktoptemplate:
        avg_rating = ReviewDesktoptemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDesktoptemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "desktoptemplate":desktoptemplate
    }
    return render(request, 'web/cplusdesktopapp.html',context)

def electrondesktopapp(request):
    desktoptemplate = Desktoptemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in desktoptemplate:
        avg_rating = ReviewDesktoptemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDesktoptemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "desktoptemplate":desktoptemplate
    }
    return render(request, 'web/electrondesktopapp.html',context)

def swiftdesktopapp(request):
    desktoptemplate = Desktoptemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in desktoptemplate:
        avg_rating = ReviewDesktoptemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDesktoptemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "desktoptemplate":desktoptemplate
    }
    return render(request, 'web/swiftdesktopapp.html',context)

def rustdesktopapp(request):
    desktoptemplate = Desktoptemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in desktoptemplate:
        avg_rating = ReviewDesktoptemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDesktoptemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "desktoptemplate":desktoptemplate
    }
    return render(request, 'web/rustdesktopapp.html',context)


# @login_required(login_url='signin')
def microsofttemplate(request):
    return render(request, 'web/microsofttemplate.html')

# @login_required(login_url='signin')
def wordtemplate(request):
    microsofttemplate = Microsofttemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in microsofttemplate:
        avg_rating = ReviewMicrosofttemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMicrosofttemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "microsofttemplate":microsofttemplate
    }
    return render(request, 'web/wordtemplate.html',context)

# @login_required(login_url='signin')
def excelltemplate(request):
    microsofttemplate = Microsofttemplate.objects.order_by('?')
    
     # Prepare data for each template
    for template in microsofttemplate:
        avg_rating = ReviewMicrosofttemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMicrosofttemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "microsofttemplate":microsofttemplate
    }
    return render(request, 'web/excelltemplate.html',context)

# @login_required(login_url='signin')
def powerpointtemplate(request):
    microsofttemplate = Microsofttemplate.objects.order_by('?')
    
     # Prepare data for each template
    for template in microsofttemplate:
        avg_rating = ReviewMicrosofttemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMicrosofttemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "microsofttemplate":microsofttemplate
    }
    return render(request, 'web/powerpointtemplate.html',context)

# @login_required(login_url='signin')
def publishertemplate(request):
    microsofttemplate = Microsofttemplate.objects.order_by('?')
    
     # Prepare data for each template
    for template in microsofttemplate:
        avg_rating = ReviewMicrosofttemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMicrosofttemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "microsofttemplate":microsofttemplate
    }
    return render(request, 'web/publishertemplate.html',context)


# @login_required(login_url='signin')
def adobetemplate(request):
    return render(request, 'web/adobetemplate.html')

# @login_required(login_url='signin')
def photoshoptemplate(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/photoshoptemplate.html',context)

# @login_required(login_url='signin')
def primiertemplate(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/primiertemplate.html',context)

# @login_required(login_url='signin')
def illustratortemplate(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/illustratortemplate.html',context)


def InDesignadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/InDesignadobe.html',context)
def XDadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/XDadobe.html',context)
def Lightroomadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Lightroomadobe.html',context)
def LightroomClassicadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/LightroomClassicadobe.html',context)
def AfterEffectsadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/AfterEffectsadobe.html',context)

def Animateadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Animateadobe.html',context)
def Dreamweaveradobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Dreamweaveradobe.html',context)
def Auditionadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Auditionadobe.html',context)
def Bridgeadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Bridgeadobe.html',context)
def Dimensionadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Dimensionadobe.html',context)

def Frescoadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Frescoadobe.html',context)
def CharacterAnimatoradobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/CharacterAnimatoradobe.html',context)
def MediaEncoderadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/MediaEncoderadobe.html',context)
def Rushadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Rushadobe.html',context)
def Sparkadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Sparkadobe.html',context)

def Substance3DPainteradobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Substance3DPainteradobe.html',context)
def Substance3DDesigneradobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Substance3DDesigneradobe.html',context)
def Substance3DSampleradobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Substance3DSampleradobe.html',context)
def Substance3DStageradobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Substance3DStageradobe.html',context)
def AcrobatProDCadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/AcrobatProDCadobe.html',context)

def Signadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Signadobe.html',context)
def FrameMakeradobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/FrameMakeradobe.html',context)
def Engageadobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Engageadobe.html',context)
def Presenteradobe(request):
    adobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in adobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
        
    context={
        "adobetemplate":adobetemplate
    }
    return render(request, 'web/Presenteradobe.html',context)

# FOR BOOK
def novels(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/novels.html',context)

def short_stories(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/short_stories.html',context)

def poetry(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/poetry.html',context)

def flash_fiction(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/flash_fiction.html',context)

def self_help_book(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/self_help_book.html',context)

def biographies(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/biographies.html',context)

def personal_development_books(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/personal_development_books.html',context)

def history_books(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/history_books.html',context)

def true_crime(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/true_crime.html',context)

def textbooks(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/textbooks.html',context)

def research_papers(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/research_papers.html',context)

def study_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/study_guides.html',context)

def how_to_guides_tutorials(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/how_to_guides_tutorials.html',context)

def business_strategy_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/business_strategy_guides.html',context)

def marketing_and_sales_e_books(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/marketing_and_sales_e_books.html',context)

def entrepreneurship_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/entrepreneurship_guides.html',context)

def financial_planning(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/financial_planning.html',context)

def nutrition_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/nutrition_guides.html',context)

def workout_and_fitness_plans(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/workout_and_fitness_plans.html',context)

def mental_health_wellness(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/mental_health_wellness.html',context)

def meditation_and_mindfulness_e_books(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/meditation_and_mindfulness_e_books.html',context)

def coding_and_programming_tutorials(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/coding_and_programming_tutorials.html',context)

def software_manuals(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/software_manuals.html',context)

def IT_and_networking_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/IT_and_networking_guides.html',context)

def artificial_intelligence_machine_learning(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/artificial_intelligence_machine_learning.html',context)

def photography_tutorials(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/photography_tutorials.html',context)

def painting_and_drawing_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/painting_and_drawing_guides.html',context)

def writing_and_storytelling_techniques(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/writing_and_storytelling_techniques.html',context)

def crafting_DIY_projects(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/crafting_DIY_projects.html',context)

def recipe_collections(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/recipe_collections.html',context)

def specialized_diet_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/specialized_diet_guides.html',context)

def meal_planning_and_prep(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/meal_planning_and_prep.html',context)

def parenting_advice(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/parenting_advice.html',context)

def marriage_and_relationship_counseling(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/marriage_and_relationship_counseling.html',context)

def family_planning_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/family_planning_guides.html',context)

def childcare_and_development(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/childcare_and_development.html',context)

def travel_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/travel_guides.html',context)

def destination_reviews(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/destination_reviews.html',context)

def adventure_stories(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/adventure_stories.html',context)

def travel_planning_and_budgeting(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/travel_planning_and_budgeting.html',context)

def personal_finance_e_books(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/personal_finance_e_books.html',context)

def investment_strategies(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/investment_strategies.html',context)

def retirement_planning(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/retirement_planning.html',context)

def budgeting_tips(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/budgeting_tips.html',context)

def religious_texts(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/religious_texts.html',context)

def spiritual_growth_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/spiritual_growth_guides.html',context)

def meditation_and_mindfulness_books(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/meditation_and_mindfulness_books.html',context)

def philosophy_and_life_purpose_e_books(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/philosophy_and_life_purpose_e_books.html',context)

def time_management_and_productivity(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/time_management_and_productivity.html',context)

def self_improvement_and_motivation(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/self_improvement_and_motivation.html',context)

def life_coaching_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/life_coaching_guides.html',context)

def work_life_balance(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/work_life_balance.html',context)

def legal_guides_and_contracts(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/legal_guides_and_contracts.html',context)

def HR_and_employment_handbooks(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/HR_and_employment_handbooks.html',context)

def professional_development(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/professional_development.html',context)

def real_estate_investment_guides(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/real_estate_investment_guides.html',context)

def property_management_manuals(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/property_management_manuals.html',context)

def buying_and_selling_homes(request):
    product = Book.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/buying_and_selling_homes.html',context)



# FOR Music & Audio
def single_tracks(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/single_tracks.html',context)


def full_albums(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/full_albums.html',context)

def extended_plays(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/extended_plays.html',context)

def instrumental_versions(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/instrumental_versions.html',context)

def beats_for_rappers_and_singers(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/beats_for_rappers_and_singers.html',context)

def lo_fi_beats(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/lo_fi_beats.html',context)

def background_instrumentals_for_videos(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/background_instrumentals_for_videos.html',context)

def royalty_free_music(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/royalty_free_music.html',context)

def environmental_sounds(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/environmental_sounds.html',context)

def foley_sounds(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/foley_sounds.html',context)

def sci_fi_and_futuristic_sounds(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/sci_fi_and_futuristic_sounds.html',context)

def horror_and_thriller_effects(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/horror_and_thriller_effects.html',context)

def drum_loops(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/drum_loops.html',context)

def melodic_loops(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/melodic_loops.html',context)

def vocal_samples(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/vocal_samples.html',context)

def synth_and_bass_loops(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/synth_and_bass_loops.html',context)


def background_music_for_videos(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/background_music_for_videos.html',context)

def music_for_podcasts(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/music_for_podcasts.html',context)

def royalty_free_soundtracks_for_commercials(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/royalty_free_soundtracks_for_commercials.html',context)

def ambient_music_for_relaxation_and_meditation(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/ambient_music_for_relaxation_and_meditation.html',context)

def talk_shows(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/talk_shows.html',context)

def interview_series(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/interview_series.html',context)

def educational_podcasts(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/educational_podcasts.html',context)

def storytelling_and_fictional_audio_series(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/storytelling_and_fictional_audio_series.html',context)

def nature_inspired_soundscapes(request):
    product = Music.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/nature_inspired_soundscapes.html',context)


# FOR Videos & Multimedia
def nature_and_landscape_footage(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/nature_and_landscape_footage.html',context)

def urban_and_city_life_footage(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/urban_and_city_life_footage.html',context)

def aerial_drone_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/aerial_drone_videos.html',context)

def slow_motion_and_time_lapse_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/slow_motion_and_time_lapse_videos.html',context)

def intros_and_outros_for_YouTube_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/intros_and_outros_for_YouTube_videos.html',context)

def two_animations(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/two_animations.html',context)

def three_animations(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/three_animations.html',context)

def explainer_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/explainer_videos.html',context)

def motion_graphics_for_commercials(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/motion_graphics_for_commercials.html',context)

def personal_vlogs(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/personal_vlogs.html',context)

def travel_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/travel_videos.html',context)

def lifestyl_vlogs(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/lifestyl_vlogs.html',context)

def daily_video_blogs(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/daily_video_blogs.html',context)

def wedding_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/wedding_videos.html',context)

def corporate_event_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/corporate_event_videos.html',context)

def party_and_celebration_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/party_and_celebration_videos.html',context)

def award_ceremony_Video(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/award_ceremony_Video.html',context)

def business_presentations(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/business_presentations.html',context)

def sales_pitches(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/sales_pitches.html',context)

def educational_or_academic_presentations(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/educational_or_academic_presentations.html',context)

def product_promo_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/product_promo_videos.html',context)

def service_advertisement_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/service_advertisement_videos.html',context)

def brand_story_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/brand_story_videos.html',context)

def social_media_ads(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/social_media_ads.html',context)

def official_music_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/official_music_videos.html',context)

def lyric_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/lyric_videos.html',context)

def animated_music_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/animated_music_videos.html',context)

def performance_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/performance_videos.html',context)

def fiction_short_films(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/fiction_short_films.html',context)

def mini_documentaries(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/mini_documentaries.html',context)

def biographical_documentaries(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/biographical_documentaries.html',context)

def indie_films(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/indie_films.html',context)

def adventure_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/adventure_videos.html',context)

def interactive_tutorials(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/interactive_tutorials.html',context)

def interactive_quizzes_or_assessments(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/interactive_quizzes_or_assessments.html',context)



def gamified_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/gamified_videos.html',context)
def customer_testimonial_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/customer_testimonial_videos.html',context)
def product_review_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/product_review_videos.html',context)
def user_generated_content_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/user_generated_content_videos.html',context)
def virtual_reality_experiences(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/virtual_reality_experiences.html',context)
def degree_video_tours(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/degree_video_tours.html',context)
def immersive_event_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/immersive_event_videos.html',context)
def cinematic_sequences(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/cinematic_sequences.html',context)
def aerial_drone_footage(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/aerial_drone_footage.html',context)
def scenic_landscape_shots(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/scenic_landscape_shots.html',context)
def epic_slow_motion_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/epic_slow_motion_videos.html',context)
def urban_timelapse_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/urban_timelapse_videos.html',context)
def nature_and_sky_timelapse(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/nature_and_sky_timelapse.html',context)
def construction_progress_timelapse(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/construction_progress_timelapse.html',context)
def yoga_and_meditation_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/yoga_and_meditation_videos.html',context)
def healthy_lifestyle_tips(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/healthy_lifestyle_tips.html',context)
def exercise_and_wellness_programs(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/exercise_and_wellness_programs.html',context)
def product_feature_demonstrations(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/product_feature_demonstrations.html',context)
def physical_product_unboxing_and_reviews(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/physical_product_unboxing_and_reviews.html',context)
def animated_YouTube_intros(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/animated_YouTube_intros.html',context)
def branding_outros_for_videos(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/branding_outros_for_videos.html',context)

def social_media_content_intros(request):
    product = Multimedia.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/social_media_content_intros.html',context)





#  FOR Digital Art & Design
def hand_drawn_digital_illustrations(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/hand_drawn_digital_illustrations.html',context)

def character_design(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/character_design.html',context)

def website_design_templates(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/website_design_templates.html',context)

def mobile_app_design_templates(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/mobile_app_design_templates.html',context)

def editorial_illustrations(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/editorial_illustrations.html',context)

def children_book_illustrations(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/children_book_illustrations.html',context)

def posters(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/posters.html',context)

def flyers(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/flyers.html',context)

def brochures(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/brochures.html',context)

def infographics(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/infographics.html',context)

def digital_advertisements(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/digital_advertisements.html',context)

def brand_logos(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/brand_logos.html',context)

def icon_sets(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/icon_sets.html',context)

def custom_logos_for_businesses(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/custom_logos_for_businesses.html',context)

def monograms(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/monograms.html',context)

def scalable_vector_illustrations(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/scalable_vector_illustrations.html',context)

def flat_design_elements(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/flat_design_elements.html',context)

def icons_and_symbols(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/icons_and_symbols.html',context)

def geometric_patterns(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/geometric_patterns.html',context)

def three_models(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/three_models.html',context)

def three_character_design(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/three_character_design.html',context)

def product_visualizations(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/product_visualizations.html',context)

def custom_fonts(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/custom_fonts.html',context)

def hand_lettering_designs(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/hand_lettering_designs.html',context)

def calligraphy_artwork(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/calligraphy_artwork.html',context)

def display_typefaces(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/display_typefaces.html',context)

def wireframe_kits(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/wireframe_kits.html',context)

def prototype_designs(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/prototype_designs.html',context)

def interactive_mockups(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/interactive_mockups.html',context)

def business_cards(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/business_cards.html',context)

def wedding_invitations(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/wedding_invitations.html',context)

def greeting_cards(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/greeting_cards.html',context)

def calendars(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/calendars.html',context)

def planners(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/planners.html',context)

def seamless_patterns(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/seamless_patterns.html',context)

def textile_and_fabric_patterns(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/textile_and_fabric_patterns.html',context)

def wallpaper_designs(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/wallpaper_designs.html',context)

def packaging_patterns(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/packaging_patterns.html',context)

def UI_UX_icons(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/UI_UX_icons.html',context)

def app_icons(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/app_icons.html',context)

def social_media_icons(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/social_media_icons.html',context)

def custom_icon_sets_for_websites(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/custom_icon_sets_for_websites.html',context)

def realistic_portrait_paintings(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/realistic_portrait_paintings.html',context)

def fantasy_landscape_paintings(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/fantasy_landscape_paintings.html',context)

def Concept_art_for_games_or_films(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/Concept_art_for_games_or_films.html',context)

def abstract_digital_artwork(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/abstract_digital_artwork.html',context)

def composite_photo_art(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/composite_photo_art.html',context)

def surreal_photo_manipulations(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/surreal_photo_manipulations.html',context)

def product_photo_retouching(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/product_photo_retouching.html',context)


def fashion_and_beauty_retouching(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/fashion_and_beauty_retouching.html',context)

def digital_collages(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/digital_collages.html',context)

def mixed_media_art(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/mixed_media_art.html',context)

def scrapbook_designs(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/scrapbook_designs.html',context)

def character_concept_art(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/character_concept_art.html',context)

def creature_and_monster_designs(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/creature_and_monster_designs.html',context)

def storyboard_art(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/storyboard_art.html',context)

def comic_book_illustrations(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/comic_book_illustrations.html',context)

def manga_style_characters_and_story_panels(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/manga_style_characters_and_story_panels.html',context)

def digital_comic_strips(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/digital_comic_strips.html',context)

def t_shirt_graphics_and_mockups(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/t_shirt_graphics_and_mockups.html',context)

def custom_merchandise_designs(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/custom_merchandise_designs.html',context)

def apparel_patterns_and_prints(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/apparel_patterns_and_prints.html',context)

def themed_photo_collections(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/themed_photo_collections.html',context)

def high_resolution_stock_images(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/high_resolution_stock_images.html',context)

def conceptual_photography(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/conceptual_photography.html',context)

def art_prints_for_home_decor(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/art_prints_for_home_decor.html',context)

def motivational_posters(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/motivational_posters.html',context)

def abstract_and_minimalist_art(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/abstract_and_minimalist_art.html',context)

def instagram_post_templates(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/instagram_post_templates.html',context)



def facebook_banner_designs(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/facebook_banner_designs.html',context)

def pinterest_graphic_templates(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/pinterest_graphic_templates.html',context)

def story_highlight_icons(request):
    product = DigitalArt.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/story_highlight_icons.html',context)


# 3D & CAD Designs
def character_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/character_models.html',context)

def vehicle_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/vehicle_models.html',context)

def furniture_and_home_decor_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/furniture_and_home_decor_models.html',context)

def product_prototypes(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/product_prototypes.html',context)

def house_and_building_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/house_and_building_designs.html',context)

def interior_and_exterior_architectural_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/interior_and_exterior_architectural_models.html',context)

def floor_plans_and_layouts(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/floor_plans_and_layouts.html',context)

def urban_planning_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/urban_planning_models.html',context)

def architectural_renderings(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/architectural_renderings.html',context)

def toys_and_figurines(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/toys_and_figurines.html',context)

def custom_jewelry_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/custom_jewelry_designs.html',context)

def gadgets_and_accessories(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/gadgets_and_accessories.html',context)

def home_decor_and_functional_objects(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/home_decor_and_functional_objects.html',context)

def mechanical_part_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/mechanical_part_designs.html',context)

def industrial_equipment_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/industrial_equipment_models.html',context)

def engineering_diagrams(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/engineering_diagrams.html',context)

def CNC_and_laser_cutting_templates(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/CNC_and_laser_cutting_templates.html',context)

def modern_and_classic_furniture_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/modern_and_classic_furniture_models.html',context)

def kitchen_and_bathroom_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/kitchen_and_bathroom_designs.html',context)

def custom_cabinetry_and_shelving_units(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/custom_cabinetry_and_shelving_units.html',context)

def threed_room_and_space_layouts(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/threed_room_and_space_layouts.html',context)

def consumer_electronics_prototypes(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/consumer_electronics_prototypes.html',context)

def fashion_and_accessory_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/fashion_and_accessory_designs.html',context)

def home_appliance_prototypes(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/home_appliance_prototypes.html',context)

def wearable_technology_prototypes(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/wearable_technology_prototypes.html',context)

def threed_characters_and_creatures(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/threed_characters_and_creatures.html',context)

def environmental_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/environmental_models.html',context)

def wweapons_and_gear(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/wweapons_and_gear.html',context)

def vehicle_models_for_gaming(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/vehicle_models_for_gaming.html',context)

def anatomy_and_body_part_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/anatomy_and_body_part_models.html',context)

def molecular_and_chemical_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/molecular_and_chemical_models.html',context)

def medical_equipment_and_device_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/medical_equipment_and_device_designs.html',context)

def scientific_visualization_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/scientific_visualization_models.html',context)

def car_and_truck_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/car_and_truck_models.html',context)

def aircraft_and_drone_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/aircraft_and_drone_designs.html',context)

def ship_and_boat_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/ship_and_boat_models.html',context)

def public_transportation_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/public_transportation_models.html',context)

def ring_and_earring_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/ring_and_earring_designs.html',context)

def pendant_and_necklace_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/pendant_and_necklace_models.html',context)

def custom_and_personalized_jewelry_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/custom_and_personalized_jewelry_designs.html',context)

def threed_printable_jewelry_prototypes(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/threed_printable_jewelry_prototypes.html',context)

def VR_ready_three_models_for_virtual_environments(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/VR_ready_three_models_for_virtual_environments.html',context)

def AR_models_for_apps_and_interactive_experiences(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/AR_models_for_apps_and_interactive_experiences.html',context)

def architectural_walkthroughs_for_VR(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/architectural_walkthroughs_for_VR.html',context)

def heavy_machinery_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/heavy_machinery_models.html',context)

def industrial_equipment(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/industrial_equipment.html',context)

def mechanical_components_and_assemblies(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/mechanical_components_and_assemblies.html',context)

def fantasy_and_sci_fi_character_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/fantasy_and_sci_fi_character_models.html',context)

def cartoon_and_stylized_characters(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/cartoon_and_stylized_characters.html',context)

def monster_and_creature_models_for_games_and_films(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/monster_and_creature_models_for_games_and_films.html',context)

def A_threed_clothing_and_accessory_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/A_threed_clothing_and_accessory_models.html',context)

def fashion_prototypes_for_manufacturing(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/fashion_prototypes_for_manufacturing.html',context)

def shoe_and_bag_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/shoe_and_bag_designs.html',context)

def fully_rigged_threed_characters_for_animation(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/fully_rigged_threed_characters_for_animation.html',context)

def motion_capture_ready_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/motion_capture_ready_models.html',context)

def custom_rigging_setups_for_specific_software(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/custom_rigging_setups_for_specific_software.html',context)

def natural_landscapes(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/natural_landscapes.html',context)

def city_and_urban_environments(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/city_and_urban_environments.html',context)

def virtual_environments_for_games_and_simulations(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/virtual_environments_for_games_and_simulations.html',context)

def engine_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/engine_models.html',context)

def gear_and_mechanical_component_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/gear_and_mechanical_component_designs.html',context)

def CAD_files_for_mechanical_systems(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/CAD_files_for_mechanical_systems.html',context)

def DIY_assembly_instructions_for_furniture(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/DIY_assembly_instructions_for_furniture.html',context)

def custom_furniture_designs_with_CAD_plans(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/custom_furniture_designs_with_CAD_plans.html',context)

def CNC_cut_plans_for_modular_furniture(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/CNC_cut_plans_for_modular_furniture.html',context)

def threed_models_of_props_for_film_sets(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/threed_models_of_props_for_film_sets.html',context)

def sci_fi_or_fantasy_set_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/sci_fi_or_fantasy_set_designs.html',context)

def historical_prop_replicas(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/historical_prop_replicas.html',context)

def robot_design_and_assembly_plans(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/robot_design_and_assembly_plans.html',context)

def drone_and_UAV_designs(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/drone_and_UAV_designs.html',context)

def industrial_automation_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/industrial_automation_models.html',context)

def A_threed_clothing_and_accessory_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/A_threed_clothing_and_accessory_models.html',context)


def threed_floor_plans(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/threed_floor_plans.html',context)

def interior_and_exterior_visualization(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/interior_and_exterior_visualization.html',context)

def threed_topographical_maps(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/threed_topographical_maps.html',context)

def terrain_models_for_games_and_simulations(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/terrain_models_for_games_and_simulations.html',context)

def landscape_elevation_models(request):
    product = CAD.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/landscape_elevation_models.html',context)

# Printable & Customizable Content
def invitations_and_greeting_cards_templates(request):
    product = Printable.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewPrintable.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewPrintable.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/invitations_and_greeting_cards_templates.html',context)

def business_cards_template(request):
    product = Printable.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewPrintable.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewPrintable.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/business_cards_template.html',context)

def wedding_templates(request):
    product = Printable.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewPrintable.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewPrintable.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/wedding_templates.html',context)

def digital_planners(request):
    product = Printable.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewPrintable.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewPrintable.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/digital_planners.html',context)

def SEO_tools(request):
    product = Printable.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewPrintable.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewPrintable.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/SEO_tools.html',context)

def email_marketing_templates(request):
    product = Printable.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewPrintable.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewPrintable.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/email_marketing_templates.html',context)

def website_themes(request):
    product = Printable.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewPrintable.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewPrintable.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/website_themes.html',context)

def custom_scripts(request):
    product = Printable.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewPrintable.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewPrintable.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/custom_scripts.html',context)


# Software & Tools
def software_applications(request):
    product = Software.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewSoftware.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewSoftware.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/software_applications.html',context)

def plugins_and_extensions(request):
    product = Software.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewSoftware.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewSoftware.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/plugins_and_extensions.html',context)

def architectural_plans(request):
    product = Software.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewSoftware.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewSoftware.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/architectural_plans.html',context)

def mobile_apps(request):
    product = Software.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewSoftware.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewSoftware.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/mobile_apps.html',context)

def software_as_a_Service(request):
    product = Software.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewSoftware.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewSoftware.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/software_as_a_Service.html',context)

def copywriting_templates(request):
    product = Software.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewSoftware.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewSoftware.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/copywriting_templates.html',context)


# Business & Marketing Tools
def business_templates(request):
    product = Business.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBusiness.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBusiness.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/business_templates.html',context)

def marketing_materials(request):
    product = Business.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBusiness.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBusiness.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/marketing_materials.html',context)

def analytics_tools(request):
    product = Business.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBusiness.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBusiness.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/analytics_tools.html',context)

def CRM_templates(request):
    product = Business.objects.order_by('?')
    
    # Prepare data for each template
    for template in product:
        avg_rating = ReviewBusiness.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBusiness.objects.filter(template=template).count()  # Total reviews
        
    context={
        "product":product
    }
    return render(request, 'web/CRM_templates.html',context)

def allproduct(request):
    productproject = Project.objects.order_by('?')
    productimage = Image.objects.order_by('?')
    productbook = Book.objects.order_by('?')
    productprintable = Printable.objects.order_by('?')
    productmusic = Music.objects.order_by('?')
    productmultmedia = Multimedia.objects.order_by('?')
    productdigitalart = DigitalArt.objects.order_by('?')
    productcad = CAD.objects.order_by('?')
    productsoftware = Software.objects.order_by('?')
    productbusiness = Business.objects.order_by('?')
    productwebsitetemplate = Websitetemplate.objects.order_by('?')
    productmobiletemplate = Mobiletemplate.objects.order_by('?')
    productdesktoptemplate = Desktoptemplate.objects.order_by('?')
    productmicrosofttemplate = Microsofttemplate.objects.order_by('?')
    productadobetemplate = Adobetemplate.objects.order_by('?')
    
    # Prepare data for each template
    for template in productproject:
        avg_rating = ReviewProject.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewProject.objects.filter(template=template).count()  # Total reviews
        
    for template in productimage:
        avg_rating = ReviewImage.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewImage.objects.filter(template=template).count()  # Total reviews
        
    for template in productbook:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    for template in productprintable:
        avg_rating = ReviewPrintable.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewPrintable.objects.filter(template=template).count()  # Total reviews
        
    for template in productmusic:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    for template in productmultmedia:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    for template in productdigitalart:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    for template in productcad:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    for template in productsoftware:
        avg_rating = ReviewSoftware.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewSoftware.objects.filter(template=template).count()  # Total reviews
        
    for template in productbusiness:
        avg_rating = ReviewBusiness.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBusiness.objects.filter(template=template).count()  # Total reviews
        
    for template in productwebsitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    for template in productmobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    for template in productdesktoptemplate:
        avg_rating = ReviewDesktoptemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDesktoptemplate.objects.filter(template=template).count()  # Total reviews
        
    for template in productmicrosofttemplate:
        avg_rating = ReviewMicrosofttemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMicrosofttemplate.objects.filter(template=template).count()  # Total reviews
        
    for template in productadobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
    
    
    context={
        "productproject":productproject,
        "productimage":productimage,
        "productbook":productbook,
        "productprintable":productprintable,
        "productmusic":productmusic,
        "productmultmedia":productmultmedia,
        "productdigitalart":productdigitalart,
        "productcad":productcad,
        "productsoftware":productsoftware,
        "productbusiness":productbusiness,
        "productwebsitetemplate":productwebsitetemplate,
        "productmobiletemplate":productmobiletemplate,
        "productdesktoptemplate":productdesktoptemplate,
        "productmicrosofttemplate":productmicrosofttemplate,
        "productadobetemplate":productadobetemplate,
    }
    return render(request, 'web/allproduct.html',context)

def template(request):
    return render(request, 'web/template.html')
def project(request):
    return render(request, 'web/project.html')
def course(request):
    return render(request, 'web/course.html')
def ebooks(request):
    return render(request, 'web/ebooks.html')
def music(request):
    return render(request, 'web/music.html')
def video(request):
    return render(request, 'web/video.html')
def art(request):
    return render(request, 'web/art.html')
def cad(request):
    return render(request, 'web/cad.html')
def printable(request):
    return render(request, 'web/printable.html')
def software(request):
    return render(request, 'web/software.html')
def business(request):
    return render(request, 'web/business.html')


# FOR MY PRODUCT
@login_required(login_url='signin')
def myproduct(request):
    current_user = request.user
    website = Website.objects.filter(user=current_user)
    mobile = Mobile.objects.filter(user=current_user)
    desktop = Desktop.objects.filter(user=current_user)
    embeded = Embeded.objects.filter(user=current_user)
    graphics = Graphics.objects.filter(user=current_user)
    project = Project.objects.filter(user=current_user)
    image = Image.objects.filter(user=current_user)
    websitetemplate = Websitetemplate.objects.filter(user=current_user)
    mobiletemplate = Mobiletemplate.objects.filter(user=current_user)
    desktoptemplate = Desktoptemplate.objects.filter(user=current_user)
    microsofttemplate = Microsofttemplate.objects.filter(user=current_user)
    adobetemplate = Adobetemplate.objects.filter(user=current_user)

    book = Book.objects.filter(user=current_user)
    printable = Printable.objects.filter(user=current_user)
    music = Music.objects.filter(user=current_user)
    multmedia = Multimedia.objects.filter(user=current_user)
    digitalArt = DigitalArt.objects.filter(user=current_user)
    cad = CAD.objects.filter(user=current_user)
    software = Software.objects.filter(user=current_user)
    business = Business.objects.filter(user=current_user)
 
    context = {
        "website": website,
        "mobile": mobile,
        "desktop": desktop,
        "embeded": embeded,
        "graphics": graphics,
        "project": project,
        "image": image,
        "websitetemplate": websitetemplate,
        "mobiletemplate": mobiletemplate,
        "desktoptemplate": desktoptemplate,
        "microsofttemplate": microsofttemplate,
        "adobetemplate": adobetemplate,
        
        "book": book,
        "printable": printable,
        "music": music,
        "multmedia": multmedia,
        "digitalArt": digitalArt,
        "cad": cad,
        "software": software,
        "business": business,
    }
    return render(request, 'web/myproduct.html', context)


# for posting the course and the template to the website
@login_required(login_url='signin')
def websitepost(request):
    websitepost = WebsiteForm()
    if request.method == "POST":
        websitepost = WebsiteForm(request.POST, files=request.FILES)
        if websitepost.is_valid():
            website = websitepost.save(commit=False)
            website.user = request.user
            websitepost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('websitepost')
    context={
        "websitepost":websitepost
    }
    return render(request, 'web/websitepost.html',context)

@login_required(login_url='signin')
def mobilepost(request):
    mobilepost = MobileForm()
    if request.method == "POST":
        mobilepost = MobileForm(request.POST, files=request.FILES)
        if mobilepost.is_valid():
            mobile = mobilepost.save(commit=False)
            mobile.user = request.user
            mobilepost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('mobilepost')
    context={
        "mobilepost":mobilepost
    }
    return render(request, 'web/mobilepost.html',context)

@login_required(login_url='signin')
def desktoppost(request):
    desktoppost = DesktopForm()
    if request.method == "POST":
        desktoppost = DesktopForm(request.POST, files=request.FILES)
        if desktoppost.is_valid():
            desktop = desktoppost.save(commit=False)
            desktop.user = request.user
            desktoppost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('desktoppost')
    context={
        "desktoppost":desktoppost
    }
    return render(request, 'web/desktoppost.html',context)

@login_required(login_url='signin')
def embededpost(request):
    embededpost = EmbededForm()
    if request.method == "POST":
        embededpost = EmbededForm(request.POST, files=request.FILES)
        if embededpost.is_valid():
            embeded = embededpost.save(commit=False)
            embeded.user = request.user
            embededpost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('embededpost')
    context={
        "embededpost":embededpost
    }
    return render(request, 'web/embededpost.html',context)

@login_required(login_url='signin')
def graphicspost(request):
    graphicspost = GraphicsForm()
    if request.method == "POST":
        graphicspost = GraphicsForm(request.POST, files=request.FILES)
        if graphicspost.is_valid():
            graphics = graphicspost.save(commit=False)
            graphics.user = request.user
            graphicspost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('graphicspost')
    context={
        "graphicspost":graphicspost
    }
    return render(request, 'web/graphicspost.html',context)

# POST PROJECT
@login_required(login_url='signin')
def projectpost(request):
    projectpost = ProjectForm()
    if request.method == "POST":
        projectpost = ProjectForm(request.POST, files=request.FILES)
        if projectpost.is_valid():
            project = projectpost.save(commit=False)
            project.user = request.user
            projectpost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('projectpost')
    context={
        "projectpost":projectpost
    }
    return render(request, 'web/projectpost.html',context)

# POST IMAGE
@login_required(login_url='signin')
def imagepost(request):
    imagepost = ImageForm()
    if request.method == "POST":
        imagepost = ImageForm(request.POST, files=request.FILES)
        if imagepost.is_valid():
            image = imagepost.save(commit=False)
            image.user = request.user
            imagepost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('imagepost')
    context={
        "imagepost":imagepost
    }
    return render(request, 'web/imagepost.html',context)



# POSTING OTHER DIGITAL PRODUCT
@login_required(login_url='signin')
def bookpost(request):
    productpost = BookForm()
    if request.method == "POST":
        productpost = BookForm(request.POST, files=request.FILES)
        if productpost.is_valid():
            product = productpost.save(commit=False)
            product.user = request.user
            productpost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('bookpost')
    context={
        "productpost":productpost
    }
    return render(request, 'web/bookpost.html',context)

@login_required(login_url='signin')
def printablepost(request):
    productpost = PrintableForm()
    if request.method == "POST":
        productpost = PrintableForm(request.POST, files=request.FILES)
        if productpost.is_valid():
            product = productpost.save(commit=False)
            product.user = request.user
            productpost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('printablepost')
    context={
        "productpost":productpost
    }
    return render(request, 'web/printablepost.html',context)

@login_required(login_url='signin')
def musicpost(request):
    productpost = MusicForm()
    if request.method == "POST":
        productpost = MusicForm(request.POST, files=request.FILES)
        if productpost.is_valid():
            product = productpost.save(commit=False)
            product.user = request.user
            productpost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('musicpost')
    context={
        "productpost":productpost
    }
    return render(request, 'web/musicpost.html',context)

@login_required(login_url='signin')
def multimediapost(request):
    productpost = MultimediaForm()
    if request.method == "POST":
        productpost = MultimediaForm(request.POST, files=request.FILES)
        if productpost.is_valid():
            product = productpost.save(commit=False)
            product.user = request.user
            productpost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('multimediapost')
    context={
        "productpost":productpost
    }
    return render(request, 'web/multimediapost.html',context)

@login_required(login_url='signin')
def digitalArtpost(request):
    productpost = DigitalArtForm()
    if request.method == "POST":
        productpost = DigitalArtForm(request.POST, files=request.FILES)
        if productpost.is_valid():
            product = productpost.save(commit=False)
            product.user = request.user
            productpost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('digitalArtpost')
    context={
        "productpost":productpost
    }
    return render(request, 'web/digitalArtpost.html',context)

@login_required(login_url='signin')
def CADpost(request):
    productpost = CADForm()
    if request.method == "POST":
        productpost = CADForm(request.POST, files=request.FILES)
        if productpost.is_valid():
            product = productpost.save(commit=False)
            product.user = request.user
            productpost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('CADpost')
    context={
        "productpost":productpost
    }
    return render(request, 'web/CADpost.html',context)

@login_required(login_url='signin')
def softwarepost(request):
    productpost = SoftwareForm()
    if request.method == "POST":
        productpost = SoftwareForm(request.POST, files=request.FILES)
        if productpost.is_valid():
            product = productpost.save(commit=False)
            product.user = request.user
            productpost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('softwarepost')
    context={
        "productpost":productpost
    }
    return render(request, 'web/softwarepost.html',context)

@login_required(login_url='signin')
def businesspost(request):
    productpost = BusinessForm()
    if request.method == "POST":
        productpost = BusinessForm(request.POST, files=request.FILES)
        if productpost.is_valid():
            product = productpost.save(commit=False)
            product.user = request.user
            productpost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('businesspost')
    context={
        "productpost":productpost
    }
    return render(request, 'web/businesspost.html',context)


# for posting template
@login_required(login_url='signin')
def websitetemplatepost(request):
    websitetemplatepost = WebsitetemplateForm()
    if request.method == "POST":
        websitetemplatepost = WebsitetemplateForm(request.POST, files=request.FILES)
        if websitetemplatepost.is_valid():
            websitetemplate = websitetemplatepost.save(commit=False)
            websitetemplate.user = request.user
            websitetemplatepost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('websitetemplatepost')
    context={
        "websitetemplatepost":websitetemplatepost
    }
    return render(request, 'web/websitetemplatepost.html',context)

@login_required(login_url='signin')
def mobiletemplatepost(request):
    mobiletemplatepost = MobiletetemplateForm()
    if request.method == "POST":
        mobiletemplatepost = MobiletetemplateForm(request.POST, files=request.FILES)
        if mobiletemplatepost.is_valid():
            mobiletemplate = mobiletemplatepost.save(commit=False)
            mobiletemplate.user = request.user
            mobiletemplatepost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('mobiletemplatepost')
    context={
        "mobiletemplatepost":mobiletemplatepost
    }
    return render(request, 'web/mobiletemplatepost.html',context)

@login_required(login_url='signin')
def desktoptemplatepost(request):
    desktoptemplatepost = DesktoptemplateForm()
    if request.method == "POST":
        desktoptemplatepost = DesktoptemplateForm(request.POST, files=request.FILES)
        if desktoptemplatepost.is_valid():
            desktoptemplate = desktoptemplatepost.save(commit=False)
            desktoptemplate.user = request.user
            desktoptemplatepost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('desktoptemplatepost')
    context={
        "desktoptemplatepost":desktoptemplatepost
    }
    return render(request, 'web/desktoptemplatepost.html',context)

@login_required(login_url='signin')
def microsofttemplatepost(request):
    microsofttemplatepost = MicrosofttemplateForm()
    if request.method == "POST":
        microsofttemplatepost = MicrosofttemplateForm(request.POST, files=request.FILES)
        if microsofttemplatepost.is_valid():
            microsofttemplate = microsofttemplatepost.save(commit=False)
            microsofttemplate.user = request.user
            microsofttemplatepost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('microsofttemplatepost')
    context={
        "microsofttemplatepost":microsofttemplatepost
    }
    return render(request, 'web/microsofttemplatepost.html',context)

@login_required(login_url='signin')
def adobeposttemplate(request):
    adobeposttemplate = AdobetemplateForm()
    if request.method == "POST":
        adobeposttemplate = AdobetemplateForm(request.POST, files=request.FILES)
        if adobeposttemplate.is_valid():
            adobetemplate = adobeposttemplate.save(commit=False)
            adobetemplate.user = request.user
            adobeposttemplate.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('adobeposttemplate')
    context={
        "adobeposttemplate":adobeposttemplate
    }
    return render(request, 'web/adobeposttemplate.html',context)


class viewwebsite(DetailView):
    model = Website
    template_name = 'web/viewwebsite.html'
    comment_form_class = CommentwebsiteForm
    payment_form_class = PaymentWebsiteForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewwebsite", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentwebsite = PaymentWebsite.objects.create(
                    user=request.user,
                    website=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD

                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentwebsite.unique_code)
                request.session['amount_in_USD'] = f"{paymentwebsite.amount:.2f}"
                request.session['payment_type'] = "website"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentwebsite URL with required parameters
                return redirect(reverse('paymentwebsite', kwargs={
                    'course_id': self.object.id,
                }))
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentwebsite.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentWebsite.objects.filter(user=self.request.user, website=self.object).last()
            if payment:
                payment_status = payment.payment_status
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
        })
        return context

    
class viewmobile(DetailView):
    model = Mobile
    template_name = 'web/viewmobile.html'
    comment_form_class = CommentmobileForm
    payment_form_class = PaymentMobileForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewmobile", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentmobile = PaymentMobile.objects.create(
                    user=request.user,
                    mobile=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentmobile.unique_code)
                request.session['amount_in_USD'] = f"{paymentmobile.amount:.2f}"
                request.session['payment_type'] = "mobile"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentmobile URL with required parameters
                return redirect(reverse('paymentmobile', kwargs={
                    'course_id': self.object.id,
                }))
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentmobile.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentMobile.objects.filter(user=self.request.user, mobile=self.object).last()
            if payment:
                payment_status = payment.payment_status
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
        })
        return context

    
class viewdesktop(DetailView):
    model = Desktop
    template_name = 'web/viewdesktop.html'
    comment_form_class = CommentdesktopForm
    payment_form_class = PaymentDesktopForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewdesktop", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentdesktop = PaymentDesktop.objects.create(
                    user=request.user,
                    desktop=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentdesktop.unique_code)
                request.session['amount_in_USD'] = f"{paymentdesktop.amount:.2f}"
                request.session['payment_type'] = "desktop"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentdesktop URL with required parameters
                return redirect(reverse('paymentdesktop', kwargs={
                    'course_id': self.object.id,
                }))
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentdesktop.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentDesktop.objects.filter(user=self.request.user, desktop=self.object).last()
            if payment:
                payment_status = payment.payment_status
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
        })
        return context



class viewembeded(DetailView):
    model = Embeded
    template_name = 'web/viewembeded.html'
    comment_form_class = CommentembededForm
    payment_form_class = PaymentEmbededForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewembeded", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentembeded = PaymentEmbeded.objects.create(
                    user=request.user,
                    embeded=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentembeded.unique_code)
                request.session['amount_in_USD'] = f"{paymentembeded.amount:.2f}"
                request.session['payment_type'] = "embeded"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentembeded URL with required parameters
                return redirect(reverse('paymentembeded', kwargs={
                    'course_id': self.object.id,
                }))
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentembeded.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentEmbeded.objects.filter(user=self.request.user, embeded=self.object).last()
            if payment:
                payment_status = payment.payment_status
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
        })
        return context



class viewgraphics(DetailView):
    model = Graphics
    template_name = 'web/viewgraphics.html'
    comment_form_class = CommentgraphicsForm
    payment_form_class = PaymentGraphicsForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewgraphics", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentgraphics = PaymentGraphics.objects.create(
                    user=request.user,
                    graphics=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentgraphics.unique_code)
                request.session['amount_in_USD'] = f"{paymentgraphics.amount:.2f}"
                request.session['payment_type'] = "graphics"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentgraphics URL with required parameters
                return redirect(reverse('paymentgraphics', kwargs={
                    'course_id': self.object.id,
                }))
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentgraphics.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentGraphics.objects.filter(user=self.request.user, graphics=self.object).last()
            if payment:
                payment_status = payment.payment_status
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
        })
        return context


# VIEW FOR VIEWING PROJECT
class viewproject(DetailView):
    model = Project
    template_name = 'web/viewproject.html'
    comment_form_class = CommentprojectForm
    payment_form_class = PaymentProjectForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewproject", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentproject = PaymentProject.objects.create(
                    user=request.user,
                    project=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentproject.unique_code)
                request.session['amount_in_USD'] = f"{paymentproject.amount:.2f}"
                request.session['payment_type'] = "project"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentproject URL with required parameters
                return redirect(reverse('paymentproject', kwargs={
                    'product_id': self.object.id,
                }))
        # Handle rating submission
        elif 'rating' in request.POST:
            rating = request.POST.get('rating')
            if rating and rating.isdigit():
                rating = int(rating)
                if 1 <= rating <= 5:  # Validate the rating value
                    review, created = ReviewProject.objects.get_or_create(
                        user=request.user,
                        template=self.object,  # Assuming the model matches Image
                        defaults={'rating': rating}
                    )
                    if not created:
                        # Update the rating if the review already exists
                        review.rating = rating
                        review.save()
                    messages.success(request, "Your rating has been submitted.")
                else:
                    messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            return redirect(reverse("viewproject", kwargs={'pk': self.object.pk}))

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentproject.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentProject.objects.filter(user=self.request.user, project=self.object).last()
            if payment:
                payment_status = payment.payment_status
                
        # Calculate average rating and count
        reviews = ReviewProject.objects.filter(template=self.object)
        avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        total_reviews = reviews.count()
        
        # Compute full stars and empty stars
        full_stars = int(floor(avg_rating))
        empty_stars = 5 - full_stars
                
        # Get random product
        random_product = Project.objects.order_by('?')[:3]
        
        # Fetch other products by the same author, excluding the current image
        more_web_templates = Websitetemplate.objects.filter(user=self.object.user)
        more_project_products = Project.objects.filter(user=self.object.user).exclude(id=self.object.id)
        more_image_products = Image.objects.filter(user=self.object.user)
        more_mobiletemplate_products = Mobiletemplate.objects.filter(user=self.object.user)
        more_desktoptemplate_products = Desktoptemplate.objects.filter(user=self.object.user)
        more_microsofttemplate_products = Microsofttemplate.objects.filter(user=self.object.user)
        more_adobetemplate_products = Adobetemplate.objects.filter(user=self.object.user)
        more_book_products = Book.objects.filter(user=self.object.user)
        more_printable_products = Printable.objects.filter(user=self.object.user)
        more_music_products = Music.objects.filter(user=self.object.user)
        more_multimedia_products = Multimedia.objects.filter(user=self.object.user)
        more_digitalart_products = DigitalArt.objects.filter(user=self.object.user)
        more_cad_products = CAD.objects.filter(user=self.object.user)
        more_software_products = Software.objects.filter(user=self.object.user)
        more_business_products = Business.objects.filter(user=self.object.user)

        # Combine all products into one list and select up to 3 randomly
        more_from_author = list(chain(
            more_web_templates,
            more_project_products,
            more_image_products,
            more_mobiletemplate_products,
            more_desktoptemplate_products,
            more_microsofttemplate_products,
            more_adobetemplate_products,
            more_book_products,
            more_printable_products,
            more_music_products,
            more_multimedia_products,
            more_digitalart_products,
            more_cad_products,
            more_software_products,
            more_business_products
        ))
        more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
        
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
            'random_product': random_product,
            'more_from_author': more_from_author,
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
            'full_stars': full_stars,
            'empty_stars': empty_stars,
        })
        return context
    
    
    
# VIEWS FOR VIEWING DIGITAL PRODUCTS
class viewbook(DetailView):
    model = Book
    template_name = 'web/viewbook.html'
    comment_form_class = CommentbookForm
    payment_form_class = PaymentBookForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewbook", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentbook = PaymentBook.objects.create(
                    user=request.user,
                    book=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentbook.unique_code)
                request.session['amount_in_USD'] = f"{paymentbook.amount:.2f}"
                request.session['payment_type'] = "book"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentproject URL with required parameters
                return redirect(reverse('paymentbook', kwargs={
                    'product_id': self.object.id,
                }))
        # Handle rating submission
        elif 'rating' in request.POST:
            rating = request.POST.get('rating')
            if rating and rating.isdigit():
                rating = int(rating)
                if 1 <= rating <= 5:  # Validate the rating value
                    review, created = ReviewBook.objects.get_or_create(
                        user=request.user,
                        template=self.object,  # Assuming the model matches Image
                        defaults={'rating': rating}
                    )
                    if not created:
                        # Update the rating if the review already exists
                        review.rating = rating
                        review.save()
                    messages.success(request, "Your rating has been submitted.")
                else:
                    messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            return redirect(reverse("viewbook", kwargs={'pk': self.object.pk}))

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentbook.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentBook.objects.filter(user=self.request.user, book=self.object).last()
            if payment:
                payment_status = payment.payment_status
                
        # Calculate average rating and count
        reviews = ReviewBook.objects.filter(template=self.object)
        avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        total_reviews = reviews.count()
        
        # Compute full stars and empty stars
        full_stars = int(floor(avg_rating))
        empty_stars = 5 - full_stars

        # Get random product
        random_product = Book.objects.order_by('?')[:3]
        
        # Fetch other products by the same author, excluding the current image
        more_web_templates = Websitetemplate.objects.filter(user=self.object.user)
        more_project_products = Project.objects.filter(user=self.object.user)
        more_image_products = Image.objects.filter(user=self.object.user)
        more_mobiletemplate_products = Mobiletemplate.objects.filter(user=self.object.user)
        more_desktoptemplate_products = Desktoptemplate.objects.filter(user=self.object.user)
        more_microsofttemplate_products = Microsofttemplate.objects.filter(user=self.object.user)
        more_adobetemplate_products = Adobetemplate.objects.filter(user=self.object.user)
        more_book_products = Book.objects.filter(user=self.object.user).exclude(id=self.object.id)
        more_printable_products = Printable.objects.filter(user=self.object.user)
        more_music_products = Music.objects.filter(user=self.object.user)
        more_multimedia_products = Multimedia.objects.filter(user=self.object.user)
        more_digitalart_products = DigitalArt.objects.filter(user=self.object.user)
        more_cad_products = CAD.objects.filter(user=self.object.user)
        more_software_products = Software.objects.filter(user=self.object.user)
        more_business_products = Business.objects.filter(user=self.object.user)

        # Combine all products into one list and select up to 3 randomly
        more_from_author = list(chain(
            more_web_templates,
            more_project_products,
            more_image_products,
            more_mobiletemplate_products,
            more_desktoptemplate_products,
            more_microsofttemplate_products,
            more_adobetemplate_products,
            more_book_products,
            more_printable_products,
            more_music_products,
            more_multimedia_products,
            more_digitalart_products,
            more_cad_products,
            more_software_products,
            more_business_products
        ))
        more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
        
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
            'random_product': random_product,
            'more_from_author': more_from_author,
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
            'full_stars': full_stars,
            'empty_stars': empty_stars,
        })
        return context
    
class viewprintable(DetailView):
    model = Printable
    template_name = 'web/viewprintable.html'
    comment_form_class = CommentprintableForm
    payment_form_class = PaymentPrintableForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewprintable", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentproduct = PaymentPrintable.objects.create(
                    user=request.user,
                    product=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentproduct.unique_code)
                request.session['amount_in_USD'] = f"{paymentproduct.amount:.2f}"
                request.session['payment_type'] = "printable"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentproject URL with required parameters
                return redirect(reverse('paymentprintable', kwargs={
                    'product_id': self.object.id,
                }))
        # Handle rating submission
        elif 'rating' in request.POST:
            rating = request.POST.get('rating')
            if rating and rating.isdigit():
                rating = int(rating)
                if 1 <= rating <= 5:  # Validate the rating value
                    review, created = ReviewPrintable.objects.get_or_create(
                        user=request.user,
                        template=self.object,  # Assuming the model matches Image
                        defaults={'rating': rating}
                    )
                    if not created:
                        # Update the rating if the review already exists
                        review.rating = rating
                        review.save()
                    messages.success(request, "Your rating has been submitted.")
                else:
                    messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            return redirect(reverse("viewprintable", kwargs={'pk': self.object.pk}))

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentprintable.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentPrintable.objects.filter(user=self.request.user, product=self.object).last()
            if payment:
                payment_status = payment.payment_status
                
        # Calculate average rating and count
        reviews = ReviewPrintable.objects.filter(template=self.object)
        avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        total_reviews = reviews.count()
        
        # Compute full stars and empty stars
        full_stars = int(floor(avg_rating))
        empty_stars = 5 - full_stars
                
        # Get random product
        random_product = Printable.objects.order_by('?')[:3]
        
        # Fetch other products by the same author, excluding the current image
        more_web_templates = Websitetemplate.objects.filter(user=self.object.user)
        more_project_products = Project.objects.filter(user=self.object.user)
        more_image_products = Image.objects.filter(user=self.object.user)
        more_mobiletemplate_products = Mobiletemplate.objects.filter(user=self.object.user)
        more_desktoptemplate_products = Desktoptemplate.objects.filter(user=self.object.user)
        more_microsofttemplate_products = Microsofttemplate.objects.filter(user=self.object.user)
        more_adobetemplate_products = Adobetemplate.objects.filter(user=self.object.user)
        more_book_products = Book.objects.filter(user=self.object.user)
        more_printable_products = Printable.objects.filter(user=self.object.user).exclude(id=self.object.id)
        more_music_products = Music.objects.filter(user=self.object.user)
        more_multimedia_products = Multimedia.objects.filter(user=self.object.user)
        more_digitalart_products = DigitalArt.objects.filter(user=self.object.user)
        more_cad_products = CAD.objects.filter(user=self.object.user)
        more_software_products = Software.objects.filter(user=self.object.user)
        more_business_products = Business.objects.filter(user=self.object.user)

        # Combine all products into one list and select up to 3 randomly
        more_from_author = list(chain(
            more_web_templates,
            more_project_products,
            more_image_products,
            more_mobiletemplate_products,
            more_desktoptemplate_products,
            more_microsofttemplate_products,
            more_adobetemplate_products,
            more_book_products,
            more_printable_products,
            more_music_products,
            more_multimedia_products,
            more_digitalart_products,
            more_cad_products,
            more_software_products,
            more_business_products
        ))
        more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
        
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
            'random_product': random_product,
            'more_from_author': more_from_author,
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
            'full_stars': full_stars,
            'empty_stars': empty_stars,
        })
        return context
    
class viewmusic(DetailView):
    model = Music
    template_name = 'web/viewmusic.html'
    comment_form_class = CommentmusicForm
    payment_form_class = PaymentMusicForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewmusic", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentproduct = PaymentMusic.objects.create(
                    user=request.user,
                    product=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentproduct.unique_code)
                request.session['amount_in_USD'] = f"{paymentproduct.amount:.2f}"
                request.session['payment_type'] = "music"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentproject URL with required parameters
                return redirect(reverse('paymentmusic', kwargs={
                    'product_id': self.object.id,
                }))
        # Handle rating submission
        elif 'rating' in request.POST:
            rating = request.POST.get('rating')
            if rating and rating.isdigit():
                rating = int(rating)
                if 1 <= rating <= 5:  # Validate the rating value
                    review, created = ReviewMusic.objects.get_or_create(
                        user=request.user,
                        template=self.object,  # Assuming the model matches Image
                        defaults={'rating': rating}
                    )
                    if not created:
                        # Update the rating if the review already exists
                        review.rating = rating
                        review.save()
                    messages.success(request, "Your rating has been submitted.")
                else:
                    messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            return redirect(reverse("viewmusic", kwargs={'pk': self.object.pk}))

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentmusic.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentMusic.objects.filter(user=self.request.user, product=self.object).last()
            if payment:
                payment_status = payment.payment_status
                
        # Calculate average rating and count
        reviews = ReviewMusic.objects.filter(template=self.object)
        avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        total_reviews = reviews.count()
        
        # Compute full stars and empty stars
        full_stars = int(floor(avg_rating))
        empty_stars = 5 - full_stars
                
        # Get random product
        random_product = Music.objects.order_by('?')[:3]
        
        # Fetch other products by the same author, excluding the current image
        more_web_templates = Websitetemplate.objects.filter(user=self.object.user)
        more_project_products = Project.objects.filter(user=self.object.user)
        more_image_products = Image.objects.filter(user=self.object.user)
        more_mobiletemplate_products = Mobiletemplate.objects.filter(user=self.object.user)
        more_desktoptemplate_products = Desktoptemplate.objects.filter(user=self.object.user)
        more_microsofttemplate_products = Microsofttemplate.objects.filter(user=self.object.user)
        more_adobetemplate_products = Adobetemplate.objects.filter(user=self.object.user)
        more_book_products = Book.objects.filter(user=self.object.user)
        more_printable_products = Printable.objects.filter(user=self.object.user)
        more_music_products = Music.objects.filter(user=self.object.user).exclude(id=self.object.id)
        more_multimedia_products = Multimedia.objects.filter(user=self.object.user)
        more_digitalart_products = DigitalArt.objects.filter(user=self.object.user)
        more_cad_products = CAD.objects.filter(user=self.object.user)
        more_software_products = Software.objects.filter(user=self.object.user)
        more_business_products = Business.objects.filter(user=self.object.user)

        # Combine all products into one list and select up to 3 randomly
        more_from_author = list(chain(
            more_web_templates,
            more_project_products,
            more_image_products,
            more_mobiletemplate_products,
            more_desktoptemplate_products,
            more_microsofttemplate_products,
            more_adobetemplate_products,
            more_book_products,
            more_printable_products,
            more_music_products,
            more_multimedia_products,
            more_digitalart_products,
            more_cad_products,
            more_software_products,
            more_business_products
        ))
        more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
        
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
            'random_product': random_product,
            'more_from_author': more_from_author,
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
            'full_stars': full_stars,
            'empty_stars': empty_stars,
        })
        return context
    
class viewmultimedia(DetailView):
    model = Multimedia
    template_name = 'web/viewmultimedia.html'
    comment_form_class = CommentmultimediaForm
    payment_form_class = PaymentMultimediaForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewmultimedia", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentproduct = PaymentMultimedia.objects.create(
                    user=request.user,
                    product=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentproduct.unique_code)
                request.session['amount_in_USD'] = f"{paymentproduct.amount:.2f}"
                request.session['payment_type'] = "multimedia"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentproject URL with required parameters
                return redirect(reverse('paymentmultimedia', kwargs={
                    'product_id': self.object.id,
                }))
        # Handle rating submission
        elif 'rating' in request.POST:
            rating = request.POST.get('rating')
            if rating and rating.isdigit():
                rating = int(rating)
                if 1 <= rating <= 5:  # Validate the rating value
                    review, created = ReviewMultimedia.objects.get_or_create(
                        user=request.user,
                        template=self.object,  # Assuming the model matches Image
                        defaults={'rating': rating}
                    )
                    if not created:
                        # Update the rating if the review already exists
                        review.rating = rating
                        review.save()
                    messages.success(request, "Your rating has been submitted.")
                else:
                    messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            return redirect(reverse("viewmultimedia", kwargs={'pk': self.object.pk}))

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentmultimedia.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentMultimedia.objects.filter(user=self.request.user, product=self.object).last()
            if payment:
                payment_status = payment.payment_status
                
        # Calculate average rating and count
        reviews = ReviewMultimedia.objects.filter(template=self.object)
        avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        total_reviews = reviews.count()
        
        # Compute full stars and empty stars
        full_stars = int(floor(avg_rating))
        empty_stars = 5 - full_stars
                
                
        # Get random product
        random_product = Multimedia.objects.order_by('?')[:3]
        
        # Fetch other products by the same author, excluding the current image
        more_web_templates = Websitetemplate.objects.filter(user=self.object.user)
        more_project_products = Project.objects.filter(user=self.object.user)
        more_image_products = Image.objects.filter(user=self.object.user)
        more_mobiletemplate_products = Mobiletemplate.objects.filter(user=self.object.user)
        more_desktoptemplate_products = Desktoptemplate.objects.filter(user=self.object.user)
        more_microsofttemplate_products = Microsofttemplate.objects.filter(user=self.object.user)
        more_adobetemplate_products = Adobetemplate.objects.filter(user=self.object.user)
        more_book_products = Book.objects.filter(user=self.object.user)
        more_printable_products = Printable.objects.filter(user=self.object.user)
        more_music_products = Music.objects.filter(user=self.object.user)
        more_multimedia_products = Multimedia.objects.filter(user=self.object.user).exclude(id=self.object.id)
        more_digitalart_products = DigitalArt.objects.filter(user=self.object.user)
        more_cad_products = CAD.objects.filter(user=self.object.user)
        more_software_products = Software.objects.filter(user=self.object.user)
        more_business_products = Business.objects.filter(user=self.object.user)

        # Combine all products into one list and select up to 3 randomly
        more_from_author = list(chain(
            more_web_templates,
            more_project_products,
            more_image_products,
            more_mobiletemplate_products,
            more_desktoptemplate_products,
            more_microsofttemplate_products,
            more_adobetemplate_products,
            more_book_products,
            more_printable_products,
            more_music_products,
            more_multimedia_products,
            more_digitalart_products,
            more_cad_products,
            more_software_products,
            more_business_products
        ))
        more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
        
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
            'random_product': random_product,
            'more_from_author': more_from_author,
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
            'full_stars': full_stars,
            'empty_stars': empty_stars,
        })
        return context
    
class viewdigitalArt(DetailView):
    model = DigitalArt
    template_name = 'web/viewdigitalArt.html'
    comment_form_class = CommentdigitalArtForm
    payment_form_class = PaymentDigitalArtForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewdigitalArt", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentproduct = PaymentDigitalArt.objects.create(
                    user=request.user,
                    product=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentproduct.unique_code)
                request.session['amount_in_USD'] = f"{paymentproduct.amount:.2f}"
                request.session['payment_type'] = "digitalArt"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentproject URL with required parameters
                return redirect(reverse('paymentdigitalArt', kwargs={
                    'product_id': self.object.id,
                }))
        # Handle rating submission
        elif 'rating' in request.POST:
            rating = request.POST.get('rating')
            if rating and rating.isdigit():
                rating = int(rating)
                if 1 <= rating <= 5:  # Validate the rating value
                    review, created = ReviewDigitalArt.objects.get_or_create(
                        user=request.user,
                        template=self.object,  # Assuming the model matches Image
                        defaults={'rating': rating}
                    )
                    if not created:
                        # Update the rating if the review already exists
                        review.rating = rating
                        review.save()
                    messages.success(request, "Your rating has been submitted.")
                else:
                    messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            return redirect(reverse("viewdigitalArt", kwargs={'pk': self.object.pk}))

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = CommentdigitalArt.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentDigitalArt.objects.filter(user=self.request.user, product=self.object).last()
            if payment:
                payment_status = payment.payment_status
                
        # Calculate average rating and count
        reviews = ReviewDigitalArt.objects.filter(template=self.object)
        avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        total_reviews = reviews.count()
        
        # Compute full stars and empty stars
        full_stars = int(floor(avg_rating))
        empty_stars = 5 - full_stars
                
        # Get random product
        random_product = DigitalArt.objects.order_by('?')[:3]
        
        # Fetch other products by the same author, excluding the current image
        more_web_templates = Websitetemplate.objects.filter(user=self.object.user)
        more_project_products = Project.objects.filter(user=self.object.user)
        more_image_products = Image.objects.filter(user=self.object.user)
        more_mobiletemplate_products = Mobiletemplate.objects.filter(user=self.object.user)
        more_desktoptemplate_products = Desktoptemplate.objects.filter(user=self.object.user)
        more_microsofttemplate_products = Microsofttemplate.objects.filter(user=self.object.user)
        more_adobetemplate_products = Adobetemplate.objects.filter(user=self.object.user)
        more_book_products = Book.objects.filter(user=self.object.user)
        more_printable_products = Printable.objects.filter(user=self.object.user)
        more_music_products = Music.objects.filter(user=self.object.user)
        more_multimedia_products = Multimedia.objects.filter(user=self.object.user)
        more_digitalart_products = DigitalArt.objects.filter(user=self.object.user).exclude(id=self.object.id)
        more_cad_products = CAD.objects.filter(user=self.object.user)
        more_software_products = Software.objects.filter(user=self.object.user)
        more_business_products = Business.objects.filter(user=self.object.user)

        # Combine all products into one list and select up to 3 randomly
        more_from_author = list(chain(
            more_web_templates,
            more_project_products,
            more_image_products,
            more_mobiletemplate_products,
            more_desktoptemplate_products,
            more_microsofttemplate_products,
            more_adobetemplate_products,
            more_book_products,
            more_printable_products,
            more_music_products,
            more_multimedia_products,
            more_digitalart_products,
            more_cad_products,
            more_software_products,
            more_business_products
        ))
        more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
        
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
            'random_product': random_product,
            'more_from_author': more_from_author,
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
            'full_stars': full_stars,
            'empty_stars': empty_stars,
        })
        return context
    
class viewCAD(DetailView):
    model = CAD
    template_name = 'web/viewCAD.html'
    comment_form_class = CommentCADForm
    payment_form_class = PaymentCADForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewCAD", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentproduct = PaymentCAD.objects.create(
                    user=request.user,
                    product=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentproduct.unique_code)
                request.session['amount_in_USD'] = f"{paymentproduct.amount:.2f}"
                request.session['payment_type'] = "cad"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentproject URL with required parameters
                return redirect(reverse('paymentcad', kwargs={
                    'product_id': self.object.id,
                }))
        # Handle rating submission
        elif 'rating' in request.POST:
            rating = request.POST.get('rating')
            if rating and rating.isdigit():
                rating = int(rating)
                if 1 <= rating <= 5:  # Validate the rating value
                    review, created = ReviewCAD.objects.get_or_create(
                        user=request.user,
                        template=self.object,  # Assuming the model matches Image
                        defaults={'rating': rating}
                    )
                    if not created:
                        # Update the rating if the review already exists
                        review.rating = rating
                        review.save()
                    messages.success(request, "Your rating has been submitted.")
                else:
                    messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            return redirect(reverse("viewCAD", kwargs={'pk': self.object.pk}))

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = CommentCAD.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentCAD.objects.filter(user=self.request.user, product=self.object).last()
            if payment:
                payment_status = payment.payment_status
                
        # Calculate average rating and count
        reviews = ReviewCAD.objects.filter(template=self.object)
        avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        total_reviews = reviews.count()
        
        # Compute full stars and empty stars
        full_stars = int(floor(avg_rating))
        empty_stars = 5 - full_stars
                
        # Get random product
        random_product = CAD.objects.order_by('?')[:3]
        
        # Fetch other products by the same author, excluding the current image
        more_web_templates = Websitetemplate.objects.filter(user=self.object.user)
        more_project_products = Project.objects.filter(user=self.object.user)
        more_image_products = Image.objects.filter(user=self.object.user)
        more_mobiletemplate_products = Mobiletemplate.objects.filter(user=self.object.user)
        more_desktoptemplate_products = Desktoptemplate.objects.filter(user=self.object.user)
        more_microsofttemplate_products = Microsofttemplate.objects.filter(user=self.object.user)
        more_adobetemplate_products = Adobetemplate.objects.filter(user=self.object.user)
        more_book_products = Book.objects.filter(user=self.object.user)
        more_printable_products = Printable.objects.filter(user=self.object.user)
        more_music_products = Music.objects.filter(user=self.object.user)
        more_multimedia_products = Multimedia.objects.filter(user=self.object.user)
        more_digitalart_products = DigitalArt.objects.filter(user=self.object.user)
        more_cad_products = CAD.objects.filter(user=self.object.user).exclude(id=self.object.id)
        more_software_products = Software.objects.filter(user=self.object.user)
        more_business_products = Business.objects.filter(user=self.object.user)

        # Combine all products into one list and select up to 3 randomly
        more_from_author = list(chain(
            more_web_templates,
            more_project_products,
            more_image_products,
            more_mobiletemplate_products,
            more_desktoptemplate_products,
            more_microsofttemplate_products,
            more_adobetemplate_products,
            more_book_products,
            more_printable_products,
            more_music_products,
            more_multimedia_products,
            more_digitalart_products,
            more_cad_products,
            more_software_products,
            more_business_products
        ))
        more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
        
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
            'random_product': random_product,
            'more_from_author': more_from_author,
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
            'full_stars': full_stars,
            'empty_stars': empty_stars,
        })
        return context
    
class viewsoftware(DetailView):
    model = Software
    template_name = 'web/viewsoftware.html'
    comment_form_class = CommentsoftwareForm
    payment_form_class = PaymentSoftwareForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewsoftware", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentproduct = PaymentSoftware.objects.create(
                    user=request.user,
                    product=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentproduct.unique_code)
                request.session['amount_in_USD'] = f"{paymentproduct.amount:.2f}"
                request.session['payment_type'] = "software"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentproject URL with required parameters
                return redirect(reverse('paymentsoftware', kwargs={
                    'product_id': self.object.id,
                }))
        # Handle rating submission
        elif 'rating' in request.POST:
            rating = request.POST.get('rating')
            if rating and rating.isdigit():
                rating = int(rating)
                if 1 <= rating <= 5:  # Validate the rating value
                    review, created = ReviewSoftware.objects.get_or_create(
                        user=request.user,
                        template=self.object,  # Assuming the model matches Image
                        defaults={'rating': rating}
                    )
                    if not created:
                        # Update the rating if the review already exists
                        review.rating = rating
                        review.save()
                    messages.success(request, "Your rating has been submitted.")
                else:
                    messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            return redirect(reverse("viewsoftware", kwargs={'pk': self.object.pk}))

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentsoftware.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentSoftware.objects.filter(user=self.request.user, product=self.object).last()
            if payment:
                payment_status = payment.payment_status
                
        # Calculate average rating and count
        reviews = ReviewSoftware.objects.filter(template=self.object)
        avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        total_reviews = reviews.count()
        
        # Compute full stars and empty stars
        full_stars = int(floor(avg_rating))
        empty_stars = 5 - full_stars
                
        # Get random product
        random_product = Software.objects.order_by('?')[:3]
        
        # Fetch other products by the same author, excluding the current image
        more_web_templates = Websitetemplate.objects.filter(user=self.object.user)
        more_project_products = Project.objects.filter(user=self.object.user)
        more_image_products = Image.objects.filter(user=self.object.user)
        more_mobiletemplate_products = Mobiletemplate.objects.filter(user=self.object.user)
        more_desktoptemplate_products = Desktoptemplate.objects.filter(user=self.object.user)
        more_microsofttemplate_products = Microsofttemplate.objects.filter(user=self.object.user)
        more_adobetemplate_products = Adobetemplate.objects.filter(user=self.object.user)
        more_book_products = Book.objects.filter(user=self.object.user)
        more_printable_products = Printable.objects.filter(user=self.object.user)
        more_music_products = Music.objects.filter(user=self.object.user)
        more_multimedia_products = Multimedia.objects.filter(user=self.object.user)
        more_digitalart_products = DigitalArt.objects.filter(user=self.object.user)
        more_cad_products = CAD.objects.filter(user=self.object.user)
        more_software_products = Software.objects.filter(user=self.object.user).exclude(id=self.object.id)
        more_business_products = Business.objects.filter(user=self.object.user)

        # Combine all products into one list and select up to 3 randomly
        more_from_author = list(chain(
            more_web_templates,
            more_project_products,
            more_image_products,
            more_mobiletemplate_products,
            more_desktoptemplate_products,
            more_microsofttemplate_products,
            more_adobetemplate_products,
            more_book_products,
            more_printable_products,
            more_music_products,
            more_multimedia_products,
            more_digitalart_products,
            more_cad_products,
            more_software_products,
            more_business_products
        ))
        more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
        
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
            'random_product': random_product,
            'more_from_author': more_from_author,
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
            'full_stars': full_stars,
            'empty_stars': empty_stars,
        })
        return context
    
    
class viewbusiness(DetailView):
    model = Business
    template_name = 'web/viewbusiness.html'
    comment_form_class = CommentbusinessForm
    payment_form_class = PaymentBusinessForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewbusiness", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentproduct = PaymentBusiness.objects.create(
                    user=request.user,
                    product=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentproduct.unique_code)
                request.session['amount_in_USD'] = f"{paymentproduct.amount:.2f}"
                request.session['payment_type'] = "business"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentproject URL with required parameters
                return redirect(reverse('paymentbusiness', kwargs={
                    'product_id': self.object.id,
                }))
    
        # Handle rating submission
        elif 'rating' in request.POST:
            rating = request.POST.get('rating')
            if rating and rating.isdigit():
                rating = int(rating)
                if 1 <= rating <= 5:  # Validate the rating value
                    review, created = ReviewBusiness.objects.get_or_create(
                        user=request.user,
                        template=self.object,  # Assuming the model matches Image
                        defaults={'rating': rating}
                    )
                    if not created:
                        # Update the rating if the review already exists
                        review.rating = rating
                        review.save()
                    messages.success(request, "Your rating has been submitted.")
                else:
                    messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            return redirect(reverse("viewbusiness", kwargs={'pk': self.object.pk}))

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentbusiness.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentBusiness.objects.filter(user=self.request.user, product=self.object).last()
            if payment:
                payment_status = payment.payment_status
                
        # Calculate average rating and count
        reviews = ReviewBusiness.objects.filter(template=self.object)
        avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        total_reviews = reviews.count()
        
        # Compute full stars and empty stars
        full_stars = int(floor(avg_rating))
        empty_stars = 5 - full_stars
                
        # Get random product
        random_product = Business.objects.order_by('?')[:3]
        
        # Fetch other products by the same author, excluding the current image
        more_web_templates = Websitetemplate.objects.filter(user=self.object.user)
        more_project_products = Project.objects.filter(user=self.object.user)
        more_image_products = Image.objects.filter(user=self.object.user)
        more_mobiletemplate_products = Mobiletemplate.objects.filter(user=self.object.user)
        more_desktoptemplate_products = Desktoptemplate.objects.filter(user=self.object.user)
        more_microsofttemplate_products = Microsofttemplate.objects.filter(user=self.object.user)
        more_adobetemplate_products = Adobetemplate.objects.filter(user=self.object.user)
        more_book_products = Book.objects.filter(user=self.object.user)
        more_printable_products = Printable.objects.filter(user=self.object.user)
        more_music_products = Music.objects.filter(user=self.object.user)
        more_multimedia_products = Multimedia.objects.filter(user=self.object.user)
        more_digitalart_products = DigitalArt.objects.filter(user=self.object.user)
        more_cad_products = CAD.objects.filter(user=self.object.user)
        more_software_products = Software.objects.filter(user=self.object.user)
        more_business_products = Business.objects.filter(user=self.object.user).exclude(id=self.object.id)

        # Combine all products into one list and select up to 3 randomly
        more_from_author = list(chain(
            more_web_templates,
            more_project_products,
            more_image_products,
            more_mobiletemplate_products,
            more_desktoptemplate_products,
            more_microsofttemplate_products,
            more_adobetemplate_products,
            more_book_products,
            more_printable_products,
            more_music_products,
            more_multimedia_products,
            more_digitalart_products,
            more_cad_products,
            more_software_products,
            more_business_products
        ))
        more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
        
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
            'random_product': random_product,
            'random_product': random_product,
            'more_from_author': more_from_author,
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
            'full_stars': full_stars,
            'empty_stars': empty_stars,
        })
        return context
    
# VIEW FOR VIEWING IMAGE
class viewimage(DetailView):
    model = Image
    template_name = 'web/viewimage.html'
    comment_form_class = CommentimageForm
    payment_form_class = PaymentImageForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment_form.instance.Title = self.object
                comment_form.save()
                return redirect(reverse("viewimage", kwargs={'pk': self.object.pk}))
        elif 'payment_submit' in request.POST:
            payment_form = self.payment_form_class(request.POST)
            if payment_form.is_valid():
                paymentproject = PaymentImage.objects.create(
                    user=request.user,
                    image=self.object,
                    payment_status='pending',
                    amount=self.object.amount_in_USD
                )
                
                # Store necessary data in the session
                request.session['unique_code'] = str(paymentproject.unique_code)
                request.session['amount_in_USD'] = f"{paymentproject.amount:.2f}"
                request.session['payment_type'] = "image"
                request.session['Title'] = slugify(self.object.Title)
                
                # Redirect to the paymentproject URL with required parameters
                return redirect(reverse('paymentimage', kwargs={
                    'product_id': self.object.id,
                }))

        # Handle rating submission
        elif 'rating' in request.POST:
            rating = request.POST.get('rating')
            if rating and rating.isdigit():
                rating = int(rating)
                if 1 <= rating <= 5:  # Validate the rating value
                    review, created = ReviewImage.objects.get_or_create(
                        user=request.user,
                        template=self.object,  # Assuming the model matches Image
                        defaults={'rating': rating}
                    )
                    if not created:
                        # Update the rating if the review already exists
                        review.rating = rating
                        review.save()
                    messages.success(request, "Your rating has been submitted.")
                else:
                    messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
            return redirect(reverse("viewimage", kwargs={'pk': self.object.pk}))

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_comments = Commentimage.objects.filter(Title=self.object.id)
        context = super().get_context_data(**kwargs)
        
        # Get the payment status for the current user and website
        payment_status = None
        if self.request.user.is_authenticated:
            payment = PaymentImage.objects.filter(user=self.request.user, image=self.object).last()
            if payment:
                payment_status = payment.payment_status
        
        # Calculate average rating and count
        reviews = ReviewImage.objects.filter(template=self.object)
        avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
        total_reviews = reviews.count()
        
        # Compute full stars and empty stars
        full_stars = int(floor(avg_rating))
        empty_stars = 5 - full_stars

        # Rondom selection of recent image posted
        random_product = Image.objects.order_by('?')[:3]
        
        # Fetch other products by the same author, excluding the current image
        more_web_templates = Websitetemplate.objects.filter(user=self.object.user)
        more_project_products = Project.objects.filter(user=self.object.user)
        more_image_products = Image.objects.filter(user=self.object.user).exclude(id=self.object.id)
        more_mobiletemplate_products = Mobiletemplate.objects.filter(user=self.object.user)
        more_desktoptemplate_products = Desktoptemplate.objects.filter(user=self.object.user)
        more_microsofttemplate_products = Microsofttemplate.objects.filter(user=self.object.user)
        more_adobetemplate_products = Adobetemplate.objects.filter(user=self.object.user)
        more_book_products = Book.objects.filter(user=self.object.user)
        more_printable_products = Printable.objects.filter(user=self.object.user)
        more_music_products = Music.objects.filter(user=self.object.user)
        more_multimedia_products = Multimedia.objects.filter(user=self.object.user)
        more_digitalart_products = DigitalArt.objects.filter(user=self.object.user)
        more_cad_products = CAD.objects.filter(user=self.object.user)
        more_software_products = Software.objects.filter(user=self.object.user)
        more_business_products = Business.objects.filter(user=self.object.user)

        # Combine all products into one list and select up to 3 randomly
        more_from_author = list(chain(
            more_web_templates,
            more_project_products,
            more_image_products,
            more_mobiletemplate_products,
            more_desktoptemplate_products,
            more_microsofttemplate_products,
            more_adobetemplate_products,
            more_book_products,
            more_printable_products,
            more_music_products,
            more_multimedia_products,
            more_digitalart_products,
            more_cad_products,
            more_software_products,
            more_business_products
        ))
        more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
    
        context.update({
            'comment_form': self.comment_form_class(),
            'payment_form': self.payment_form_class(),
            'post_comments': post_comments,
            'payment_status': payment_status,
            'random_product': random_product,
            'more_from_author': more_from_author,
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
            'full_stars': full_stars,
            'empty_stars': empty_stars,
        })
        return context
    

@login_required(login_url='signin')
@disable_browser_cache
def viewwebsitetemplate(request, id):
    # Retrieve the website template
    websitetemplate = get_object_or_404(Websitetemplate, id=id)
    Websitetemplateview = Websitetemplate.objects.get(id=id)

    # Check if the user has made a payment for this template
    is_paid = False
    if request.user.is_authenticated:
        payment = Payment.objects.filter(user=request.user, template=websitetemplate).last()
        if payment and payment.payment_status == 'paid':
            is_paid = True
      
    # Calculate average rating and count
    reviews = ReviewWebsitetemplate.objects.filter(template=websitetemplate)
    avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
    total_reviews = reviews.count()

    # Compute full stars and empty stars
    full_stars = int(floor(avg_rating))
    empty_stars = 5 - full_stars
          
    # Handle rating submission
    if request.method == 'POST' and 'rating' in request.POST:
        rating = request.POST.get('rating')
        if rating and rating.isdigit():
            rating = int(rating)
            if 1 <= rating <= 5:  # Validate the rating value
                review, created = ReviewWebsitetemplate.objects.get_or_create(
                    user=request.user,
                    template=websitetemplate,
                    defaults={'rating': rating}
                )
                if not created:
                    # Update the rating if the review already exists
                    review.rating = rating
                    review.save()
                messages.success(request, "Your rating has been submitted.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
        else:
            messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
        return redirect('viewwebsitetemplate', id=websitetemplate.id)
            
    # Retrieve at least 5 random recent templates
    recent_templates = Websitetemplate.objects.order_by('?')[:3]
    
    # Fetch other products by the same author, excluding the current template
    more_web_templates = Websitetemplate.objects.filter(user=websitetemplate.user).exclude(id=id)
    more_Project_products = Project.objects.filter(user=websitetemplate.user)
    more_Image_products = Image.objects.filter(user=websitetemplate.user)
    more_Mobiletemplate_products = Mobiletemplate.objects.filter(user=websitetemplate.user)
    more_Desktoptemplate_products = Desktoptemplate.objects.filter(user=websitetemplate.user)
    more_Microsofttemplater_products = Microsofttemplate.objects.filter(user=websitetemplate.user)
    more_Adobetemplate_products = Adobetemplate.objects.filter(user=websitetemplate.user)
    more_Book_products = Book.objects.filter(user=websitetemplate.user)
    more_Printable_products = Printable.objects.filter(user=websitetemplate.user)
    more_Music_products = Music.objects.filter(user=websitetemplate.user)
    more_Multimedia_products = Multimedia.objects.filter(user=websitetemplate.user)
    more_DigitalArt_products = DigitalArt.objects.filter(user=websitetemplate.user)
    more_CAD_products = CAD.objects.filter(user=websitetemplate.user)
    more_Software_products = Software.objects.filter(user=websitetemplate.user)
    more_Business_products = Business.objects.filter(user=websitetemplate.user)

    
    # Combine all products into one list
    more_from_author = list(more_web_templates) + list(more_Project_products) + list(more_Image_products) + list(more_Mobiletemplate_products) + list(more_Desktoptemplate_products) + list(more_Microsofttemplater_products) + list(more_Adobetemplate_products) + list(more_Book_products) + list(more_Printable_products) + list(more_Music_products) + list(more_Multimedia_products) + list(more_DigitalArt_products) + list(more_CAD_products) + list(more_Software_products) + list(more_Business_products)
    
    # Randomly select up to 5 items from the combined list
    more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
    
    
    context = {
        "Websitetemplateview":Websitetemplateview,
        'Websitetemplateview': websitetemplate,
        'is_paid': is_paid,
        'recent_templates': recent_templates,
        'more_from_author': more_from_author,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'full_stars': range(full_stars),
        'empty_stars': range(empty_stars),
        }
    return render(request, 'web/viewwebsitetemplate.html', context)


@login_required(login_url='signin')
def viewmobiletemplate(request, id):
    mobiletemplate = get_object_or_404(Mobiletemplate, id=id)
    mobiletemplateview = Mobiletemplate.objects.get(id=id)
    
    # Check if the user has made a payment for this template
    is_paid = False
    if request.user.is_authenticated:
        payment = PaymentMobiletemplate.objects.filter(user=request.user, mobiletemplate=mobiletemplate).last()
        if payment and payment.payment_status == 'paid':
            is_paid = True
            
    # Calculate average rating and count
    reviews = ReviewMobiletemplate.objects.filter(template=mobiletemplate)
    avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
    total_reviews = reviews.count()

    # Compute full stars and empty stars
    full_stars = int(floor(avg_rating))
    empty_stars = 5 - full_stars
          
    # Handle rating submission
    if request.method == 'POST' and 'rating' in request.POST:
        rating = request.POST.get('rating')
        if rating and rating.isdigit():
            rating = int(rating)
            if 1 <= rating <= 5:  # Validate the rating value
                review, created = ReviewMobiletemplate.objects.get_or_create(
                    user=request.user,
                    template=mobiletemplate,
                    defaults={'rating': rating}
                )
                if not created:
                    # Update the rating if the review already exists
                    review.rating = rating
                    review.save()
                messages.success(request, "Your rating has been submitted.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
        else:
            messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
        return redirect('viewmobiletemplate', id=mobiletemplate.id)
            
    # Retrieve at least 5 random recent templates
    recent_templates = Mobiletemplate.objects.order_by('?')[:3]
    
    # Fetch other products by the same author, excluding the current template
    more_web_templates = Websitetemplate.objects.filter(user=mobiletemplate.user)
    more_Project_products = Project.objects.filter(user=mobiletemplate.user)
    more_Image_products = Image.objects.filter(user=mobiletemplate.user)
    more_Mobiletemplate_products = Mobiletemplate.objects.filter(user=mobiletemplate.user).exclude(id=id)
    more_Desktoptemplate_products = Desktoptemplate.objects.filter(user=mobiletemplate.user)
    more_Microsofttemplater_products = Microsofttemplate.objects.filter(user=mobiletemplate.user)
    more_Adobetemplate_products = Adobetemplate.objects.filter(user=mobiletemplate.user)
    more_Book_products = Book.objects.filter(user=mobiletemplate.user)
    more_Printable_products = Printable.objects.filter(user=mobiletemplate.user)
    more_Music_products = Music.objects.filter(user=mobiletemplate.user)
    more_Multimedia_products = Multimedia.objects.filter(user=mobiletemplate.user)
    more_DigitalArt_products = DigitalArt.objects.filter(user=mobiletemplate.user)
    more_CAD_products = CAD.objects.filter(user=mobiletemplate.user)
    more_Software_products = Software.objects.filter(user=mobiletemplate.user)
    more_Business_products = Business.objects.filter(user=mobiletemplate.user)

    
    # Combine all products into one list
    more_from_author = list(more_web_templates) + list(more_Project_products) + list(more_Image_products) + list(more_Mobiletemplate_products) + list(more_Desktoptemplate_products) + list(more_Microsofttemplater_products) + list(more_Adobetemplate_products) + list(more_Book_products) + list(more_Printable_products) + list(more_Music_products) + list(more_Multimedia_products) + list(more_DigitalArt_products) + list(more_CAD_products) + list(more_Software_products) + list(more_Business_products)
    
    # Randomly select up to 5 items from the combined list
    more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
    
    context = {
        "mobiletemplateview":mobiletemplateview,
        'mobiletemplateview': mobiletemplateview,
        'is_paid': is_paid,
        'recent_templates': recent_templates,
        'more_from_author': more_from_author,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'full_stars': range(full_stars),
        'empty_stars': range(empty_stars),
        }
    return render(request, 'web/viewmobiletemplate.html', context)


@login_required(login_url='signin')
def viewdesktoptemplate(request, id):
    desktoptemplate = get_object_or_404(Desktoptemplate, id=id)
    desktoptemplateview = Desktoptemplate.objects.get(id=id)
    
    # Check if the user has made a payment for this template
    is_paid = False
    if request.user.is_authenticated:
        payment = PaymentDesktoptemplate.objects.filter(user=request.user, desktoptemplate=desktoptemplate).last()
        if payment and payment.payment_status == 'paid':
            is_paid = True
            
    # Calculate average rating and count
    reviews = ReviewDesktoptemplate.objects.filter(template=desktoptemplate)
    avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
    total_reviews = reviews.count()

    # Compute full stars and empty stars
    full_stars = int(floor(avg_rating))
    empty_stars = 5 - full_stars
          
    # Handle rating submission
    if request.method == 'POST' and 'rating' in request.POST:
        rating = request.POST.get('rating')
        if rating and rating.isdigit():
            rating = int(rating)
            if 1 <= rating <= 5:  # Validate the rating value
                review, created = ReviewDesktoptemplate.objects.get_or_create(
                    user=request.user,
                    template=desktoptemplate,
                    defaults={'rating': rating}
                )
                if not created:
                    # Update the rating if the review already exists
                    review.rating = rating
                    review.save()
                messages.success(request, "Your rating has been submitted.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
        else:
            messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
        return redirect('viewdesktoptemplate', id=desktoptemplate.id)
            
    # Retrieve at least 5 random recent templates
    recent_templates = Desktoptemplate.objects.order_by('?')[:3]
    
    # Fetch other products by the same author, excluding the current template
    more_web_templates = Websitetemplate.objects.filter(user=desktoptemplate.user)
    more_Project_products = Project.objects.filter(user=desktoptemplate.user)
    more_Image_products = Image.objects.filter(user=desktoptemplate.user)
    more_Mobiletemplate_products = Mobiletemplate.objects.filter(user=desktoptemplate.user)
    more_Desktoptemplate_products = Desktoptemplate.objects.filter(user=desktoptemplate.user).exclude(id=id)
    more_Microsofttemplater_products = Microsofttemplate.objects.filter(user=desktoptemplate.user)
    more_Adobetemplate_products = Adobetemplate.objects.filter(user=desktoptemplate.user)
    more_Book_products = Book.objects.filter(user=desktoptemplate.user)
    more_Printable_products = Printable.objects.filter(user=desktoptemplate.user)
    more_Music_products = Music.objects.filter(user=desktoptemplate.user)
    more_Multimedia_products = Multimedia.objects.filter(user=desktoptemplate.user)
    more_DigitalArt_products = DigitalArt.objects.filter(user=desktoptemplate.user)
    more_CAD_products = CAD.objects.filter(user=desktoptemplate.user)
    more_Software_products = Software.objects.filter(user=desktoptemplate.user)
    more_Business_products = Business.objects.filter(user=desktoptemplate.user)

    
    # Combine all products into one list
    more_from_author = list(more_web_templates) + list(more_Project_products) + list(more_Image_products) + list(more_Mobiletemplate_products) + list(more_Desktoptemplate_products) + list(more_Microsofttemplater_products) + list(more_Adobetemplate_products) + list(more_Book_products) + list(more_Printable_products) + list(more_Music_products) + list(more_Multimedia_products) + list(more_DigitalArt_products) + list(more_CAD_products) + list(more_Software_products) + list(more_Business_products)
    
    # Randomly select up to 5 items from the combined list
    more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
    
    context = {
        "desktoptemplateview":desktoptemplateview,
        'desktoptemplateview': desktoptemplateview,
        'is_paid': is_paid,
        'recent_templates': recent_templates,
        'more_from_author': more_from_author,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'full_stars': range(full_stars),
        'empty_stars': range(empty_stars),
        }
    return render(request, 'web/viewdesktoptemplate.html', context)

@login_required(login_url='signin')
def viewmicrosofttemplate(request, id):
     # Retrieve the microsoft template
    microsofttemplate = get_object_or_404(Microsofttemplate, id=id)
    microsofttemplateview = Microsofttemplate.objects.get(id=id)

    # Check if the user has made a payment for this template
    is_paid = False
    if request.user.is_authenticated:
        payment = PaymentMicrosofttemplate.objects.filter(user=request.user, microsofttemplate=microsofttemplate).last()
        if payment and payment.payment_status == 'paid':
            is_paid = True
            
    # Calculate average rating and count
    reviews = ReviewMicrosofttemplate.objects.filter(template=microsofttemplate)
    avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
    total_reviews = reviews.count()

    # Compute full stars and empty stars
    full_stars = int(floor(avg_rating))
    empty_stars = 5 - full_stars
          
    # Handle rating submission
    if request.method == 'POST' and 'rating' in request.POST:
        rating = request.POST.get('rating')
        if rating and rating.isdigit():
            rating = int(rating)
            if 1 <= rating <= 5:  # Validate the rating value
                review, created = ReviewMicrosofttemplate.objects.get_or_create(
                    user=request.user,
                    template=microsofttemplate,
                    defaults={'rating': rating}
                )
                if not created:
                    # Update the rating if the review already exists
                    review.rating = rating
                    review.save()
                messages.success(request, "Your rating has been submitted.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
        else:
            messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
        return redirect('viewmicrosofttemplate', id=microsofttemplate.id)
            
    # Retrieve at least 5 random recent templates
    recent_templates = Microsofttemplate.objects.order_by('?')[:3]
    
    # Fetch other products by the same author, excluding the current template
    more_web_templates = Websitetemplate.objects.filter(user=microsofttemplate.user)
    more_Project_products = Project.objects.filter(user=microsofttemplate.user)
    more_Image_products = Image.objects.filter(user=microsofttemplate.user)
    more_Mobiletemplate_products = Mobiletemplate.objects.filter(user=microsofttemplate.user)
    more_Desktoptemplate_products = Desktoptemplate.objects.filter(user=microsofttemplate.user)
    more_Microsofttemplater_products = Microsofttemplate.objects.filter(user=microsofttemplate.user).exclude(id=id)
    more_Adobetemplate_products = Adobetemplate.objects.filter(user=microsofttemplate.user)
    more_Book_products = Book.objects.filter(user=microsofttemplate.user)
    more_Printable_products = Printable.objects.filter(user=microsofttemplate.user)
    more_Music_products = Music.objects.filter(user=microsofttemplate.user)
    more_Multimedia_products = Multimedia.objects.filter(user=microsofttemplate.user)
    more_DigitalArt_products = DigitalArt.objects.filter(user=microsofttemplate.user)
    more_CAD_products = CAD.objects.filter(user=microsofttemplate.user)
    more_Software_products = Software.objects.filter(user=microsofttemplate.user)
    more_Business_products = Business.objects.filter(user=microsofttemplate.user)

    
    # Combine all products into one list
    more_from_author = list(more_web_templates) + list(more_Project_products) + list(more_Image_products) + list(more_Mobiletemplate_products) + list(more_Desktoptemplate_products) + list(more_Microsofttemplater_products) + list(more_Adobetemplate_products) + list(more_Book_products) + list(more_Printable_products) + list(more_Music_products) + list(more_Multimedia_products) + list(more_DigitalArt_products) + list(more_CAD_products) + list(more_Software_products) + list(more_Business_products)
    
    # Randomly select up to 5 items from the combined list
    more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
    
    context = {
        "microsofttemplateview":microsofttemplateview,
        # 'microsofttemplate': microsofttemplate,
        'is_paid': is_paid,
        'recent_templates': recent_templates,
        'more_from_author': more_from_author,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'full_stars': range(full_stars),
        'empty_stars': range(empty_stars),
        }
    return render(request, 'web/viewmicrosofttemplate.html', context)


@login_required(login_url='signin')
def viewadobetemplate(request, id):
     # Retrieve the adobe template
    adobetemplate = get_object_or_404(Adobetemplate, id=id)
    adobetemplateview = Adobetemplate.objects.get(id=id)

    # Check if the user has made a payment for this template
    is_paid = False
    if request.user.is_authenticated:
        payment = PaymentAdobetemplate.objects.filter(user=request.user, adobetemplate=adobetemplate).last()
        if payment and payment.payment_status == 'paid':
            is_paid = True
            
    # Calculate average rating and count
    reviews = ReviewAdobetemplate.objects.filter(template=adobetemplate)
    avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
    total_reviews = reviews.count()

    # Compute full stars and empty stars
    full_stars = int(floor(avg_rating))
    empty_stars = 5 - full_stars
          
    # Handle rating submission
    if request.method == 'POST' and 'rating' in request.POST:
        rating = request.POST.get('rating')
        if rating and rating.isdigit():
            rating = int(rating)
            if 1 <= rating <= 5:  # Validate the rating value
                review, created = ReviewAdobetemplate.objects.get_or_create(
                    user=request.user,
                    template=adobetemplate,
                    defaults={'rating': rating}
                )
                if not created:
                    # Update the rating if the review already exists
                    review.rating = rating
                    review.save()
                messages.success(request, "Your rating has been submitted.")
            else:
                messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
        else:
            messages.error(request, "Invalid rating. Please select a value between 1 and 5.")
        return redirect('viewadobetemplate', id=adobetemplate.id)
            
    # Retrieve at least 5 random recent templates
    recent_templates = Adobetemplate.objects.order_by('?')[:3]
    
    # Fetch other products by the same author, excluding the current template
    more_web_templates = Websitetemplate.objects.filter(user=adobetemplate.user)
    more_Project_products = Project.objects.filter(user=adobetemplate.user)
    more_Image_products = Image.objects.filter(user=adobetemplate.user)
    more_Mobiletemplate_products = Mobiletemplate.objects.filter(user=adobetemplate.user)
    more_Desktoptemplate_products = Desktoptemplate.objects.filter(user=adobetemplate.user)
    more_Microsofttemplater_products = Microsofttemplate.objects.filter(user=adobetemplate.user)
    more_Adobetemplate_products = Adobetemplate.objects.filter(user=adobetemplate.user).exclude(id=id)
    more_Book_products = Book.objects.filter(user=adobetemplate.user)
    more_Printable_products = Printable.objects.filter(user=adobetemplate.user)
    more_Music_products = Music.objects.filter(user=adobetemplate.user)
    more_Multimedia_products = Multimedia.objects.filter(user=adobetemplate.user)
    more_DigitalArt_products = DigitalArt.objects.filter(user=adobetemplate.user)
    more_CAD_products = CAD.objects.filter(user=adobetemplate.user)
    more_Software_products = Software.objects.filter(user=adobetemplate.user)
    more_Business_products = Business.objects.filter(user=adobetemplate.user)

    
    # Combine all products into one list
    more_from_author = list(more_web_templates) + list(more_Project_products) + list(more_Image_products) + list(more_Mobiletemplate_products) + list(more_Desktoptemplate_products) + list(more_Microsofttemplater_products) + list(more_Adobetemplate_products) + list(more_Book_products) + list(more_Printable_products) + list(more_Music_products) + list(more_Multimedia_products) + list(more_DigitalArt_products) + list(more_CAD_products) + list(more_Software_products) + list(more_Business_products)
    
    # Randomly select up to 5 items from the combined list
    more_from_author = random.sample(more_from_author, min(len(more_from_author), 3))
    
    context = {
        "adobetemplateview":adobetemplateview,
        # 'adobetemplate': adobetemplate,
        'is_paid': is_paid,
        'recent_templates': recent_templates,
        'more_from_author': more_from_author,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'full_stars': range(full_stars),
        'empty_stars': range(empty_stars),
        }
    return render(request, 'web/viewadobetemplate.html', context)

@login_required(login_url='signin')
def viewcontact(request, id):
    contact = Contact.objects.get(id=id)
    
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    context = {
        "contact":contact,
        "notification":notification,
        "notificationcount":notificationcount,
        }
    return render(request, 'web/viewcontact.html', context)


# views for deleting the course
@login_required(login_url='signin')
def deletewebsite(request, id):
    websitedelete = Website.objects.get(id=id)
    if request.method == "POST":
        websitedelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('website')
    
    context = {"websitedelete":websitedelete}
    return render(request, 'web/deletewebsite.html', context)

@login_required(login_url='signin')
def deletemobile(request, id):
    mobiledelete = Mobile.objects.get(id=id)
    if request.method == "POST":
        mobiledelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('mobileapp')
    
    context = {"mobiledelete":mobiledelete}
    return render(request, 'web/deletemobile.html', context)

@login_required(login_url='signin')
def deletedesktop(request, id):
    desktopdelete = Desktop.objects.get(id=id)
    if request.method == "POST":
        desktopdelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('desktopapp')
    
    context = {"desktopdelete":desktopdelete}
    return render(request, 'web/deletedesktop.html', context)

@login_required(login_url='signin')
def deleteembeded(request, id):
    embededdelete = Embeded.objects.get(id=id)
    if request.method == "POST":
        embededdelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('embeded')
    
    context = {"embededdelete":embededdelete}
    return render(request, 'web/deleteembeded.html', context)

@login_required(login_url='signin')
def deletegraphics(request, id):
    graphicsdelete = Graphics.objects.get(id=id)
    if request.method == "POST":
        graphicsdelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('graphics')
    
    context = {"graphicsdelete":graphicsdelete}
    return render(request, 'web/deletegraphics.html', context)

# DELETING PROJECT
@login_required(login_url='signin')
def deleteproject(request, id):
    projectdelete = Project.objects.get(id=id)
    if request.method == "POST":
        projectdelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('graphics')
    
    context = {"projectdelete":projectdelete}
    return render(request, 'web/deleteproject.html', context)

# DELETING OTHER DIGITAL PRODUCT
@login_required(login_url='signin')
def deletebook(request, id):
    bookdelete = Book.objects.get(id=id)
    if request.method == "POST":
        bookdelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('ebooks')
    
    context = {"bookdelete":bookdelete}
    return render(request, 'web/deletebook.html', context)

@login_required(login_url='signin')
def deleteprintable(request, id):
    printabledelete = Printable.objects.get(id=id)
    if request.method == "POST":
        printabledelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('printable')
    
    context = {"printabledelete":printabledelete}
    return render(request, 'web/deleteprintable.html', context)

@login_required(login_url='signin')
def deletemusic(request, id):
    musicdelete = Music.objects.get(id=id)
    if request.method == "POST":
        musicdelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('music')
    
    context = {"musicdelete":musicdelete}
    return render(request, 'web/deletemusic.html', context)

@login_required(login_url='signin')
def deletemultimedia(request, id):
    multimediadelete = Multimedia.objects.get(id=id)
    if request.method == "POST":
        multimediadelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('multimedia')
    
    context = {"multimediadelete":multimediadelete}
    return render(request, 'web/deletemultimedia.html', context)

@login_required(login_url='signin')
def deletedigitalArt(request, id):
    digitalArtdelete = DigitalArt.objects.get(id=id)
    if request.method == "POST":
        digitalArtdelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('digitalArt')
    
    context = {"digitalArtdelete":digitalArtdelete}
    return render(request, 'web/deletedigitalArt.html', context)

@login_required(login_url='signin')
def deleteCAD(request, id):
    CADdelete = CAD.objects.get(id=id)
    if request.method == "POST":
        CADdelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('cad')
    
    context = {"CADdelete":CADdelete}
    return render(request, 'web/deleteCAD.html', context)

@login_required(login_url='signin')
def deletesoftware(request, id):
    softwaredelete = Software.objects.get(id=id)
    if request.method == "POST":
        softwaredelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('cad')
    
    context = {"softwaredelete":softwaredelete}
    return render(request, 'web/deletesoftware.html', context)

@login_required(login_url='signin')
def deletebusiness(request, id):
    businessdelete = Business.objects.get(id=id)
    if request.method == "POST":
        businessdelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('business')
    
    context = {"businessdelete":businessdelete}
    return render(request, 'web/deletebusiness.html', context)

# DELETING IMAGE
@login_required(login_url='signin')
def deleteimage(request, id):
    imagedelete = Image.objects.get(id=id)
    if request.method == "POST":
        imagedelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('image')
    
    context = {"imagedelete":imagedelete}
    return render(request, 'web/deleteimage.html', context)

# views for deleting template
@login_required(login_url='signin')
def deletewebsitetemplate(request, id):
    websitetemplatedelete = Websitetemplate.objects.get(id=id)
    if request.method == "POST":
        websitetemplatedelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('Website')
    
    context = {"websitetemplatedelete":websitetemplatedelete}
    return render(request, 'web/deletewebsitetemplate.html', context)

@login_required(login_url='signin')
def deletemobiletemplate(request, id):
    mobiletemplatedelete = Mobiletemplate.objects.get(id=id)
    if request.method == "POST":
        mobiletemplatedelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('mobiletemplate')
    
    context = {"mobiletemplatedelete":mobiletemplatedelete}
    return render(request, 'web/deletemobiletemplate.html', context)

@login_required(login_url='signin')
def deletedesktoptemplate(request, id):
    desktoptemplatedelete = Desktoptemplate.objects.get(id=id)
    if request.method == "POST":
        desktoptemplatedelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('desktoptemplate')
    
    context = {"desktoptemplatedelete":desktoptemplatedelete}
    return render(request, 'web/deletedesktoptemplate.html', context)

@login_required(login_url='signin')
def deletemicrosofttemplate(request, id):
    microsofttemplatedelete = Microsofttemplate.objects.get(id=id)
    if request.method == "POST":
        microsofttemplatedelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('microsofttemplate')
    
    context = {"microsofttemplatedelete":microsofttemplatedelete}
    return render(request, 'web/deletemicrosofttemplate.html', context)

@login_required(login_url='signin')
def deleteadobetemplate(request, id):
    adobetemplatedelete = Adobetemplate.objects.get(id=id)
    if request.method == "POST":
        adobetemplatedelete.delete()
        messages.info(request, 'Deleted succesefull.')
        return redirect('adobetemplate')
    
    context = {"adobetemplatedelete":adobetemplatedelete}
    return render(request, 'web/deleteadobetemplate.html', context)


# views for the updating course and templates
@login_required(login_url='signin')
def updatewebsite(request, id):
    a = Website.objects.get(id=id)
    website = WebsiteForm(instance=a)
    if request.method == "POST":
        website = WebsiteForm(request.POST, files=request.FILES, instance=a)
        if website.is_valid():
            website.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('website')
    context = {"website":website}
    return render(request, 'web/updatewebsite.html', context)

@login_required(login_url='signin')
def updatemobile(request, id):
    b = Mobile.objects.get(id=id)
    mobile = MobileForm(instance=b)
    if request.method == "POST":
        mobile = MobileForm(request.POST, files=request.FILES, instance=b)
        if mobile.is_valid():
            mobile.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('mobileapp')
    context = {"mobile":mobile}
    return render(request, 'web/updatemobile.html', context)

@login_required(login_url='signin')
def updatedesktop(request, id):
    c = Desktop.objects.get(id=id)
    desktop = DesktopForm(instance=c)
    if request.method == "POST":
        desktop = DesktopForm(request.POST, files=request.FILES, instance=c)
        if desktop.is_valid():
            desktop.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('desktopapp')
    context = {"desktop":desktop}
    return render(request, 'web/updatedesktop.html', context)

@login_required(login_url='signin')
def updateembeded(request, id):
    d = Embeded.objects.get(id=id)
    embeded = EmbededForm(instance=d)
    if request.method == "POST":
        embeded = EmbededForm(request.POST, files=request.FILES, instance=d)
        if embeded.is_valid():
            embeded.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('embeded')
    context = {"embeded":embeded}
    return render(request, 'web/updateembeded.html', context)

@login_required(login_url='signin')
def updategraphics(request, id):
    j = Graphics.objects.get(id=id)
    graphics = GraphicsForm(instance=j)
    if request.method == "POST":
        graphics = GraphicsForm(request.POST, files=request.FILES, instance=j)
        if graphics.is_valid():
            graphics.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('graphics')
    context = {"graphics":graphics}
    return render(request, 'web/updategraphics.html', context)


# FOR UPDATING PROJECT
@login_required(login_url='signin')
def updateproject(request, id):
    n = Project.objects.get(id=id)
    project = ProjectForm(instance=n)
    if request.method == "POST":
        project = ProjectForm(request.POST, files=request.FILES, instance=n)
        if project.is_valid():
            project.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('websiteproject')
    context = {"project":project}
    return render(request, 'web/updateproject.html', context)

# FOR UPDATING OTHER DIGITAL PRODUCT
@login_required(login_url='signin')
def updatebook(request, id):
    aa = Book.objects.get(id=id)
    book = BookForm(instance=aa)
    if request.method == "POST":
        book = BookForm(request.POST, files=request.FILES, instance=aa)
        if book.is_valid():
            book.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('ebooks')
    context = {"book":book}
    return render(request, 'web/updatebook.html', context)

@login_required(login_url='signin')
def updateprintable(request, id):
    ab = Printable.objects.get(id=id)
    printable = PrintableForm(instance=ab)
    if request.method == "POST":
        printable = PrintableForm(request.POST, files=request.FILES, instance=ab)
        if printable.is_valid():
            printable.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('printable')
    context = {"printable":printable}
    return render(request, 'web/updateprintable.html', context)

@login_required(login_url='signin')
def updatemusic(request, id):
    ac = Music.objects.get(id=id)
    music = MusicForm(instance=ac)
    if request.method == "POST":
        music = MusicForm(request.POST, files=request.FILES, instance=ac)
        if music.is_valid():
            music.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('music')
    context = {"music":music}
    return render(request, 'web/updatemusic.html', context)

@login_required(login_url='signin')
def updatemultimedia(request, id):
    ad = Multimedia.objects.get(id=id)
    multimedia = MultimediaForm(instance=ad)
    if request.method == "POST":
        multimedia = MultimediaForm(request.POST, files=request.FILES, instance=ad)
        if multimedia.is_valid():
            multimedia.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('multimedia')
    context = {"multimedia":multimedia}
    return render(request, 'web/updatemultimedia.html', context)

@login_required(login_url='signin')
def updatedigitalArt(request, id):
    ae = DigitalArt.objects.get(id=id)
    digitalArt = DigitalArtForm(instance=ae)
    if request.method == "POST":
        digitalArt = DigitalArtForm(request.POST, files=request.FILES, instance=ae)
        if digitalArt.is_valid():
            digitalArt.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('digitalArt')
    context = {"digitalArt":digitalArt}
    return render(request, 'web/updatedigitalArt.html', context)

@login_required(login_url='signin')
def updateCAD(request, id):
    af = CAD.objects.get(id=id)
    cad = CADForm(instance=af)
    if request.method == "POST":
        cad = CADForm(request.POST, files=request.FILES, instance=af)
        if cad.is_valid():
            cad.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('cad')
    context = {"cad":cad}
    return render(request, 'web/updateCAD.html', context)


@login_required(login_url='signin')
def updatesoftware(request, id):
    az = Software.objects.get(id=id)
    software = SoftwareForm(instance=az)
    if request.method == "POST":
        software = SoftwareForm(request.POST, files=request.FILES, instance=az)
        if software.is_valid():
            software.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('software')
    context = {"software":software}
    return render(request, 'web/updatesoftware.html', context)

@login_required(login_url='signin')
def updatebusiness(request, id):
    ah = Business.objects.get(id=id)
    business = BusinessForm(instance=ah)
    if request.method == "POST":
        business = BusinessForm(request.POST, files=request.FILES, instance=ah)
        if business.is_valid():
            business.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('business')
    context = {"business":business}
    return render(request, 'web/updatebusiness.html', context)

# FOR UPDATING IMAGE
@login_required(login_url='signin')
def updateimage(request, id):
    q = Image.objects.get(id=id)
    image = ImageForm(instance=q)
    if request.method == "POST":
        image = ImageForm(request.POST, files=request.FILES, instance=q)
        if image.is_valid():
            image.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('image')
    context = {"image":image}
    return render(request, 'web/updateimage.html', context)

def updatecard(request, id):
    ca = Card.objects.get(id=id)
    card = CardForm(instance=ca)
    if request.method == "POST":
        card = CardForm(request.POST, files=request.FILES, instance=ca)
        if card.is_valid():
            card.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('mycard')
    context = {"card":card}
    return render(request, 'web/updatecard.html', context)


# views for updating template
@login_required(login_url='signin')
def updatewebsitetemplate(request, id):
    e = Websitetemplate.objects.get(id=id)
    websitetemplate = WebsitetemplateForm(instance=e)
    if request.method == "POST":
        websitetemplate = WebsitetemplateForm(request.POST, files=request.FILES, instance=e)
        if websitetemplate.is_valid():
            websitetemplate.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('webtemplate')
    context = {"websitetemplate":websitetemplate}
    return render(request, 'web/updatewebsitetemplate.html', context)

@login_required(login_url='signin')
def updatemobiletemplate(request, id):
    f = Mobiletemplate.objects.get(id=id)
    mobiletemplate = MobiletetemplateForm(instance=f)
    if request.method == "POST":
        mobiletemplate = MobiletetemplateForm(request.POST, files=request.FILES, instance=f)
        if mobiletemplate.is_valid():
            mobiletemplate.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('mobiletemplate')
    context = {"mobiletemplate":mobiletemplate}
    return render(request, 'web/updatemobiletemplate.html', context)

@login_required(login_url='signin')
def updatedesktoptemplate(request, id):
    g = Desktoptemplate.objects.get(id=id)
    desktoptemplate = DesktoptemplateForm(instance=g)
    if request.method == "POST":
        desktoptemplate = DesktoptemplateForm(request.POST, files=request.FILES, instance=g)
        if desktoptemplate.is_valid():
            desktoptemplate.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('desktoptemplate')
    context = {"desktoptemplate":desktoptemplate}
    return render(request, 'web/updatedesktoptemplate.html', context)

@login_required(login_url='signin')
def updatemicrosofttemplate(request, id):
    h = Microsofttemplate.objects.get(id=id)
    microsofttemplate = MicrosofttemplateForm(instance=h)
    if request.method == "POST":
        microsofttemplate = MicrosofttemplateForm(request.POST, files=request.FILES, instance=h)
        if microsofttemplate.is_valid():
            microsofttemplate.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('microsofttemplate')
    context = {"microsofttemplate":microsofttemplate}
    return render(request, 'web/updatemicrosofttemplate.html', context)

@login_required(login_url='signin')
def updateadobetemplate(request, id):
    i = Adobetemplate.objects.get(id=id)
    adobetemplate = AdobetemplateForm(instance=i)
    if request.method == "POST":
        adobetemplate = AdobetemplateForm(request.POST, files=request.FILES, instance=i)
        if adobetemplate.is_valid():
            adobetemplate.save()
            messages.info(request, 'Updated succesefull.')
            return redirect('adobetemplate')
    context = {"adobetemplate":adobetemplate}
    return render(request, 'web/updateadobetemplate.html', context)


 
 # FOR PAYMENT OF TEMPLATES
@method_decorator(never_cache, name='dispatch')
class PaymentViewWebsitetemplate(LoginRequiredMixin, View, PaymentRequestMixin):
    template_name = "web/payment.html"

    def get(self, request, product_id):
        template = get_object_or_404(Websitetemplate, id=product_id)
        payment = Payment.objects.create(
            user=request.user,
            template=template,
            payment_status='pending',
            amount=template.amount_in_USD
        )
        request.session['unique_code'] = payment.unique_code
        request.session['amount'] = float(template.amount_in_USD)
        request.session['payment_type'] = "websitetemplate"
        order_info = {
            "amount": template.amount_in_USD * 2685,
            "description": f"Payment for {template.Title}",
            "reference": payment.id,
            "email": request.user.email,
        }
        pesapal_url = self.get_payment_url(**order_info)
        return render(request, self.template_name, {'pesapal_url': pesapal_url})

class PaymentViewMobiletemplate(LoginRequiredMixin, View, PaymentRequestMixin):
    template_name = "web/payment.html"

    def get(self, request, product_id):
        mobiletemplate = get_object_or_404(Mobiletemplate, id=product_id)
        mobiletemplatepayment = PaymentMobiletemplate.objects.create(
            user=request.user,
            mobiletemplate=mobiletemplate,
            payment_status='pending',
            amount=mobiletemplate.amount_in_USD
        )
        request.session['unique_code'] = mobiletemplatepayment.unique_code
        request.session['amount'] = float(mobiletemplate.amount_in_USD)
        request.session['payment_type'] = "mobiletemplate"
        order_info = {
            "amount": mobiletemplate.amount_in_USD * 2685,
            "description": f"Payment for {mobiletemplate.Title}",
            "reference": mobiletemplatepayment.id,
            "email": request.user.email,
        }
        pesapal_url = self.get_payment_url(**order_info)
        return render(request, self.template_name, {'pesapal_url': pesapal_url})

class PaymentViewDesktoptemplate(LoginRequiredMixin, View, PaymentRequestMixin):
    template_name = "web/payment.html"

    def get(self, request, product_id):
        desktoptemplate = get_object_or_404(Desktoptemplate, id=product_id)
        desktoptemplatepayment = PaymentDesktoptemplate.objects.create(
            user=request.user,
            desktoptemplate=desktoptemplate,
            payment_status='pending',
            amount=desktoptemplate.amount_in_USD
        )
        request.session['unique_code'] = desktoptemplatepayment.unique_code
        request.session['amount'] = float(desktoptemplate.amount_in_USD)
        request.session['payment_type'] = "desktoptemplate"
        order_info = {
            "amount": desktoptemplate.amount_in_USD * 2685,
            "description": f"Payment for {desktoptemplate.Title}",
            "reference": desktoptemplatepayment.id,
            "email": request.user.email,
        }
        pesapal_url = self.get_payment_url(**order_info)
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
class PaymentViewMicrosofttemplate(LoginRequiredMixin, View, PaymentRequestMixin):
    template_name = "web/payment.html"

    def get(self, request, product_id):
        microsofttemplate = get_object_or_404(Microsofttemplate, id=product_id)
        microsofttemplatepayment = PaymentMicrosofttemplate.objects.create(
            user=request.user,
            microsofttemplate=microsofttemplate,
            payment_status='pending',
            amount=microsofttemplate.amount_in_USD
        )
        request.session['unique_code'] = microsofttemplatepayment.unique_code
        request.session['amount'] = float(microsofttemplate.amount_in_USD)
        request.session['payment_type'] = "microsofttemplate"
        order_info = {
            "amount": microsofttemplate.amount_in_USD * 2685,
            "description": f"Payment for {microsofttemplate.Title}",
            "reference": microsofttemplatepayment.id,
            "email": request.user.email,
        }
        pesapal_url = self.get_payment_url(**order_info)
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
class PaymentViewAdobetemplate(LoginRequiredMixin, View, PaymentRequestMixin):
    template_name = "web/payment.html"

    def get(self, request, product_id):
        adobetemplate = get_object_or_404(Adobetemplate, id=product_id)
        adobetemplatepayment = PaymentAdobetemplate.objects.create(
            user=request.user,
            adobetemplate=adobetemplate,
            payment_status='pending',
            amount=adobetemplate.amount_in_USD
        )
        request.session['unique_code'] = adobetemplatepayment.unique_code
        request.session['amount'] = float(adobetemplate.amount_in_USD)
        request.session['payment_type'] = "adobetemplate"
        order_info = {
            "amount": adobetemplate.amount_in_USD * 2685,
            "description": f"Payment for {adobetemplate.Title}",
            "reference": adobetemplatepayment.id,
            "email": request.user.email,
        }
        pesapal_url = self.get_payment_url(**order_info)
        return render(request, self.template_name, {'pesapal_url': pesapal_url})



 # FOR PAYMENT OF COURSES 
@method_decorator(never_cache, name='dispatch')
class PaymentViewWebsite(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, course_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'course_id': course_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['course_id'] = course_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "website"
        # request.session['website'] = website

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": course_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})


    
class PaymentViewMobile(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, course_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'course_id': course_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['course_id'] = course_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "mobile"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": course_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})


    
class PaymentViewDesktop(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, course_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'course_id': course_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['course_id'] = course_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "desktop"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": course_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})


class PaymentViewEmbeded(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, course_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'course_id': course_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['course_id'] = course_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "embeded"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": course_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})

    
class PaymentViewGraphics(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, course_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'course_id': course_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['course_id'] = course_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "graphics"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": course_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})


    
 # VIEWS FOR PROJECT PAYMENT
class PaymentViewProject(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, product_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'product_id': product_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['product_id'] = product_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "project"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": product_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
 # VIEWS FOR DIGITAL PRODUCT PAYMENT
class PaymentViewBook(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, product_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'product_id': product_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['product_id'] = product_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "book"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": product_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
class PaymentViewPrintable(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, product_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'product_id': product_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['product_id'] = product_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "printable"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": product_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
class PaymentViewMusic(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, product_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'product_id': product_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['product_id'] = product_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "music"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": product_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
class PaymentViewMultimedia(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, product_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'product_id': product_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['product_id'] = product_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "multimedia"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": product_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
class PaymentViewDigitalArt(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, product_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'product_id': product_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['product_id'] = product_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "digitalArt"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": product_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
class PaymentViewCAD(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, product_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'product_id': product_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['product_id'] = product_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "CAD"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": product_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
class PaymentViewSoftware(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, product_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'product_id': product_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['product_id'] = product_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "software"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": product_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
    
class PaymentViewBusiness(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view 
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, product_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'product_id': product_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['product_id'] = product_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "business"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": product_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})


# VIEWS FOR IMAGE PAYMENT
class PaymentViewImage(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, product_id):
        unique_code = request.session.get('unique_code')
        Title = request.session.get('Title')
        amount = Decimal(request.session.get('amount_in_USD', '0.00'))
        
        context = {
            'product_id': product_id,
        }

        # Store the data in the session
        request.session['unique_code'] = unique_code
        request.session['product_id'] = product_id
        request.session['amount'] = float(amount)
        request.session['payment_type'] = "image"

        # Generate payment order info
        order_info = {
            "amount": amount * 2685,
            "description": f"Payment for {Title}",
            "reference": product_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
    
# UPDATING PAYMENT
def update_websitetemplatepayment_status(payment, transaction_id):
    """Update the payment status to 'paid'."""
    payment.payment_status = 'paid'
    payment.transaction_id = transaction_id
    payment.save()
    
def update_mobiletemplatepayment_status(mobiletemplatepayment, transaction_id):
    """Update the payment status to 'paid'."""
    mobiletemplatepayment.payment_status = 'paid'
    mobiletemplatepayment.transaction_id = transaction_id
    mobiletemplatepayment.save()
    
def update_desktoptemplatepayment_status(desktoptemplatepayment, transaction_id):
    """Update the payment status to 'paid'."""
    desktoptemplatepayment.payment_status = 'paid'
    desktoptemplatepayment.transaction_id = transaction_id
    desktoptemplatepayment.save()
    
def update_microsofttemplatepayment_status(microsofttemplatepayment, transaction_id):
    """Update the payment status to 'paid'."""
    microsofttemplatepayment.payment_status = 'paid'
    microsofttemplatepayment.transaction_id = transaction_id
    microsofttemplatepayment.save()
    
def update_adobetemplatepayment_status(adobetemplatepayment, transaction_id):
    """Update the payment status to 'paid'."""
    adobetemplatepayment.payment_status = 'paid'
    adobetemplatepayment.transaction_id = transaction_id
    adobetemplatepayment.save()
    
# UPDATING PAYMENT FOR COURSES
def update_websitepayment_status(websitepayment, transaction_id):
    """Update the payment status to 'paid'."""
    websitepayment.payment_status = 'paid'
    websitepayment.transaction_id = transaction_id
    websitepayment.save()
    
def update_mobilepayment_status(mobilepayment, transaction_id):
    """Update the payment status to 'paid'."""
    mobilepayment.payment_status = 'paid'
    mobilepayment.transaction_id = transaction_id
    mobilepayment.save()
    
def update_desktoppayment_status(desktoppayment, transaction_id):
    """Update the payment status to 'paid'."""
    desktoppayment.payment_status = 'paid'
    desktoppayment.transaction_id = transaction_id
    desktoppayment.save()
    
def update_embededpayment_status(embededpayment, transaction_id):
    """Update the payment status to 'paid'."""
    embededpayment.payment_status = 'paid'
    embededpayment.transaction_id = transaction_id
    embededpayment.save()
    
def update_graphicspayment_status(graphicspayment, transaction_id):
    """Update the payment status to 'paid'."""
    graphicspayment.payment_status = 'paid'
    graphicspayment.transaction_id = transaction_id
    graphicspayment.save()

# UPDATE PAYMENT FOR PROJECT
def update_projectpayment_status(projectpayment, transaction_id):
    """Update the payment status to 'paid'."""
    projectpayment.payment_status = 'paid'
    projectpayment.transaction_id = transaction_id
    projectpayment.save()
    
# UPDATE PAYMENT FOR DIGITAL PRODUCT
def update_bookpayment_status(bookpayment, transaction_id):
    """Update the payment status to 'paid'."""
    bookpayment.payment_status = 'paid'
    bookpayment.transaction_id = transaction_id
    bookpayment.save()
    
def update_printablepayment_status(printablepayment, transaction_id):
    """Update the payment status to 'paid'."""
    printablepayment.payment_status = 'paid'
    printablepayment.transaction_id = transaction_id
    printablepayment.save()
    
def update_musicpayment_status(musicpayment, transaction_id):
    """Update the payment status to 'paid'."""
    musicpayment.payment_status = 'paid'
    musicpayment.transaction_id = transaction_id
    musicpayment.save()
    
def update_multimediapayment_status(multimediapayment, transaction_id):
    """Update the payment status to 'paid'."""
    multimediapayment.payment_status = 'paid'
    multimediapayment.transaction_id = transaction_id
    multimediapayment.save()
    
def update_digitalArtpayment_status(digitalArtpayment, transaction_id):
    """Update the payment status to 'paid'."""
    digitalArtpayment.payment_status = 'paid'
    digitalArtpayment.transaction_id = transaction_id
    digitalArtpayment.save()
    
def update_CADpayment_status(CADpayment, transaction_id):
    """Update the payment status to 'paid'."""
    CADpayment.payment_status = 'paid'
    CADpayment.transaction_id = transaction_id
    CADpayment.save()
    
def update_softwarepayment_status(softwarepayment, transaction_id):
    """Update the payment status to 'paid'."""
    softwarepayment.payment_status = 'paid'
    softwarepayment.transaction_id = transaction_id
    softwarepayment.save()
    
def update_businesspayment_status(businesspayment, transaction_id):
    """Update the payment status to 'paid'."""
    businesspayment.payment_status = 'paid'
    businesspayment.transaction_id = transaction_id
    businesspayment.save()
    
# UPDATE PAYMENT FOR IMAGE
def update_imagepayment_status(imagepayment, transaction_id):
    """Update the payment status to 'paid'."""
    imagepayment.payment_status = 'paid'
    imagepayment.transaction_id = transaction_id
    imagepayment.save()
    
    
#HANDLING PAYMENT
@disable_browser_cache
def handle_websitetemplate_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    payment = Payment.objects.filter(user=request.user).last()
    if payment:
        template_id = payment.template.id
        payment = get_object_or_404(Payment, template_id=template_id, unique_code=unique_code, user=request.user)
        update_websitetemplatepayment_status(payment, transaction_id)
        # process_websitetemplate_purchase(request, template_id)
        return redirect(reverse('process_websitetemplate_purchase', args=[template_id]))
    return None

def handle_mobiletemplate_payment(request, transaction_id, unique_code):
    """Handle mobile template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    mobiletemplatepayment = PaymentMobiletemplate.objects.filter(user=request.user).last()
    if mobiletemplatepayment:
        mobiletemplate_id = mobiletemplatepayment.mobiletemplate.id
        mobiletemplatepayment = get_object_or_404(PaymentMobiletemplate, mobiletemplate_id=mobiletemplate_id, unique_code=unique_code, user=request.user)
        update_mobiletemplatepayment_status(mobiletemplatepayment, transaction_id)
        # process_mobiletemplate_purchase(request, mobiletemplate_id)
        return redirect(reverse('process_mobiletemplate_purchase', args=[mobiletemplate_id]))
    return None

def handle_desktoptemplate_payment(request, transaction_id, unique_code):
    """Handle desktop template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    desktoptemplatepayment = PaymentDesktoptemplate.objects.filter(user=request.user).last()
    if desktoptemplatepayment:
        desktoptemplate_id = desktoptemplatepayment.desktoptemplate.id
        desktoptemplatepayment = get_object_or_404(PaymentDesktoptemplate, desktoptemplate_id=desktoptemplate_id, unique_code=unique_code, user=request.user)
        update_desktoptemplatepayment_status(desktoptemplatepayment, transaction_id)
        #process_desktoptemplate_purchase(request, desktoptemplate_id)
        return redirect(reverse('process_desktoptemplate_purchase', args=[desktoptemplate_id]))
    return None

def handle_microsofttemplate_payment(request, transaction_id, unique_code):
    """Handle mobile template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    microsofttemplatepayment = PaymentMicrosofttemplate.objects.filter(user=request.user).last()
    if microsofttemplatepayment:
        microsofttemplate_id = mobiletemplatepayment.mobiletemplate.id
        mobiletemplatepayment = get_object_or_404(PaymentMicrosofttemplate, microsofttemplate_id=microsofttemplate_id, unique_code=unique_code, user=request.user)
        update_microsofttemplatepayment_status(microsofttemplatepayment, transaction_id)
        # process_microsofttemplate_purchase(request, microsofttemplate_id)
        return redirect(reverse('process_microsofttemplate_purchase', args=[microsofttemplate_id]))
    return None

def handle_adobetemplate_payment(request, transaction_id, unique_code):
    """Handle desktop template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    adobetemplatepayment = PaymentAdobetemplate.objects.filter(user=request.user).last()
    if adobetemplatepayment:
        adobetemplate_id = adobetemplatepayment.adobetemplate.id
        adobetemplatepayment = get_object_or_404(PaymentAdobetemplate, adobetemplate_id=adobetemplate_id, unique_code=unique_code, user=request.user)
        update_adobetemplatepayment_status(adobetemplatepayment, transaction_id)
        # process_adobetemplate_purchase(request, adobetemplate_id)
        return redirect(reverse('process_adobetemplate_purchase', args=[adobetemplate_id]))
    return None

#HANDLING PAYMENT FOR COURSES
def handle_website_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    websitepayment = PaymentWebsite.objects.filter(user=request.user).last()
    course_id = request.session.get('course_id')
    if websitepayment:
        websitepayment = get_object_or_404(PaymentWebsite,unique_code=unique_code, user=request.user)
        update_websitepayment_status(websitepayment, transaction_id)
        process_website_purchase(request, course_id)
        return redirect(reverse('viewwebsite', args=[course_id]))
    return None

def handle_mobile_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    mobilepayment = PaymentMobile.objects.filter(user=request.user).last()
    course_id = request.session.get('course_id')
    if mobilepayment:
        mobilepayment = get_object_or_404(PaymentMobile, unique_code=unique_code, user=request.user)
        update_mobilepayment_status(mobilepayment, transaction_id)
        process_mobile_purchase(request, course_id)
        return redirect(reverse('viewmobile', args=[course_id]))
    return None


def handle_desktop_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    desktoppayment = PaymentDesktop.objects.filter(user=request.user).last()
    course_id = request.session.get('course_id')
    if desktoppayment:
        desktoppayment = get_object_or_404(PaymentDesktop, unique_code=unique_code, user=request.user)
        update_desktoppayment_status(desktoppayment, transaction_id)
        process_desktop_purchase(request, course_id)
        return redirect(reverse('viewdesktop', args=[course_id]))
    return None

def handle_embeded_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    embededpayment = PaymentEmbeded.objects.filter(user=request.user).last()
    course_id = request.session.get('course_id')
    if embededpayment:
        embededpayment = get_object_or_404(PaymentEmbeded, unique_code=unique_code, user=request.user)
        update_embededpayment_status(embededpayment, transaction_id)
        process_embeded_purchase(request, course_id)
        return redirect(reverse('viewembeded', args=[course_id]))
    return None

def handle_graphics_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    graphicspayment = PaymentGraphics.objects.filter(user=request.user).last()
    course_id = request.session.get('course_id')
    if graphicspayment:
        graphicspayment = get_object_or_404(PaymentGraphics, unique_code=unique_code, user=request.user)
        update_graphicspayment_status(graphicspayment, transaction_id)
        process_graphics_purchase(request, course_id)
        return redirect(reverse('viewgraphics', args=[course_id]))
    return None

# HANDLE PAYMENT FOR PROJECT
def handle_project_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    projectpayment = PaymentProject.objects.filter(user=request.user).last()
    product_id = request.session.get('product_id')
    if projectpayment:
        projectpayment = get_object_or_404(PaymentProject, unique_code=unique_code, user=request.user)
        update_projectpayment_status(projectpayment, transaction_id)
        # process_project_purchase(request, product_id)
        return redirect(reverse('process_project_purchase', args=[product_id]))
    return None

# HANDLE PAYMENT FOR DIGITAL PRODUCT
def handle_book_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    bookpayment = PaymentBook.objects.filter(user=request.user).last()
    product_id = request.session.get('product_id')
    if bookpayment:
        bookpayment = get_object_or_404(PaymentBook, unique_code=unique_code, user=request.user)
        update_bookpayment_status(bookpayment, transaction_id)
        # process_book_purchase(request, product_id)
        return redirect(reverse('process_book_purchase', args=[product_id]))
    return None

def handle_printable_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    printablepayment = PaymentPrintable.objects.filter(user=request.user).last()
    product_id = request.session.get('product_id')
    if printablepayment:
        printablepayment = get_object_or_404(PaymentPrintable, unique_code=unique_code, user=request.user)
        update_printablepayment_status(printablepayment, transaction_id)
        # process_printable_purchase(request, product_id)
        return redirect(reverse('process_printable_purchase', args=[product_id]))
    return None

def handle_music_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    musicpayment = PaymentMusic.objects.filter(user=request.user).last()
    product_id = request.session.get('product_id')
    if musicpayment:
        musicpayment = get_object_or_404(PaymentMusic, unique_code=unique_code, user=request.user)
        update_musicpayment_status(musicpayment, transaction_id)
        # process_music_purchase(request, product_id)
        return redirect(reverse('process_music_purchase', args=[product_id]))
    return None

def handle_multimedia_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    multimediapayment = PaymentMultimedia.objects.filter(user=request.user).last()
    product_id = request.session.get('product_id')
    if multimediapayment:
        multimediapayment = get_object_or_404(PaymentMultimedia, unique_code=unique_code, user=request.user)
        update_multimediapayment_status(multimediapayment, transaction_id)
        # process_multimedia_purchase(request, product_id)
        return redirect(reverse('process_multimedia_purchase', args=[product_id]))
    return None

def handle_digitalArt_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    digitalArtpayment = PaymentDigitalArt.objects.filter(user=request.user).last()
    product_id = request.session.get('product_id')
    if digitalArtpayment:
        digitalArtpayment = get_object_or_404(PaymentDigitalArt, unique_code=unique_code, user=request.user)
        update_digitalArtpayment_status(digitalArtpayment, transaction_id)
        # process_digitalArt_purchase(request, product_id)
        return redirect(reverse('process_digitalArt_purchase', args=[product_id]))
    return None

def handle_CAD_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    CADpayment = PaymentCAD.objects.filter(user=request.user).last()
    product_id = request.session.get('product_id')
    if CADpayment:
        CADpayment = get_object_or_404(PaymentCAD, unique_code=unique_code, user=request.user)
        update_CADpayment_status(CADpayment, transaction_id)
        # process_CAD_purchase(request, product_id)
        return redirect(reverse('process_CAD_purchase', args=[product_id]))
    return None

def handle_software_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    softwarepayment = PaymentSoftware.objects.filter(user=request.user).last()
    product_id = request.session.get('product_id')
    if softwarepayment:
        softwarepayment = get_object_or_404(PaymentSoftware, unique_code=unique_code, user=request.user)
        update_softwarepayment_status(softwarepayment, transaction_id)
        # process_CAD_purchase(request, product_id)
        return redirect(reverse('process_software_purchase', args=[product_id]))
    return None

def handle_business_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    businesspayment = PaymentBusiness.objects.filter(user=request.user).last()
    product_id = request.session.get('product_id')
    if businesspayment:
        businesspayment = get_object_or_404(PaymentBusiness, unique_code=unique_code, user=request.user)
        update_businesspayment_status(businesspayment, transaction_id)
        # process_business_purchase(request, product_id)
        return redirect(reverse('process_business_purchase', args=[product_id]))
    return None

# HANDLE PAYMENT FOR IMAGE
def handle_image_payment(request, transaction_id, unique_code):
    """Handle website template payment."""
    amount = request.session.get('amount')
    request.session['amount'] = amount
    imagepayment = PaymentImage.objects.filter(user=request.user).last()
    product_id = request.session.get('product_id')
    if imagepayment:
        imagepayment = get_object_or_404(PaymentImage, unique_code=unique_code, user=request.user)
        update_imagepayment_status(imagepayment, transaction_id)
        # process_image_purchase(request, product_id)
        return redirect(reverse('process_image_purchase', args=[product_id]))
    return None

# PAYMENT COMPLETION
@disable_browser_cache
def payment_completed(request):
    transaction_id = request.GET.get('pesapal_transaction_tracking_id')
    unique_code = request.session.get('unique_code')
    payment_type = request.session.get('payment_type')
    website = request.session.get('website')
    course_id = request.session.get('course_id')
    project_id = request.session.get('project_id')
    image_id = request.session.get('image_id')
    amount = request.session.get('amount')
    
    product_id = request.session.get('product_id')
    
    
    request.session['course_id'] = course_id
    request.session['project_id'] = project_id
    request.session['image_id'] = image_id
    request.session['product_id'] = product_id
    request.session['amount'] = amount

    if payment_type == 'websitetemplate':
        response = handle_websitetemplate_payment(request, transaction_id, unique_code)
    elif payment_type == 'mobiletemplate':
        response = handle_mobiletemplate_payment(request, transaction_id, unique_code)
    elif payment_type == 'desktoptemplate':
        response = handle_desktoptemplate_payment(request, transaction_id, unique_code)
    elif payment_type == 'microsofttemplate':
        response = handle_microsofttemplate_payment(request, transaction_id, unique_code)
    elif payment_type == 'adobetemplate':
        response = handle_adobetemplate_payment(request, transaction_id, unique_code)
    elif payment_type == 'website':
        response = handle_website_payment(request, transaction_id, unique_code)
    elif payment_type == 'mobile':
        response = handle_mobile_payment(request, transaction_id, unique_code)
    elif payment_type == 'desktop':
        response = handle_desktop_payment(request, transaction_id, unique_code)
    elif payment_type == 'embeded':
        response = handle_embeded_payment(request, transaction_id, unique_code)
    elif payment_type == 'graphics':
        response = handle_graphics_payment(request, transaction_id, unique_code)
    elif payment_type == 'project':
        response = handle_project_payment(request, transaction_id, unique_code)
    elif payment_type == 'image':
        response = handle_image_payment(request, transaction_id, unique_code)
        
    elif payment_type == 'book':
        response = handle_book_payment(request, transaction_id, unique_code)
    elif payment_type == 'printable':
        response = handle_printable_payment(request, transaction_id, unique_code)
    elif payment_type == 'music':
        response = handle_music_payment(request, transaction_id, unique_code)
    elif payment_type == 'multimedia':
        response = handle_multimedia_payment(request, transaction_id, unique_code)
    elif payment_type == 'digitalArt':
        response = handle_digitalArt_payment(request, transaction_id, unique_code)
    elif payment_type == 'CAD':
        response = handle_CAD_payment(request, transaction_id, unique_code)
    elif payment_type == 'software':
        response = handle_software_payment(request, transaction_id, unique_code)
    elif payment_type == 'business':
        response = handle_business_payment(request, transaction_id, unique_code)
    else:
        return redirect('website')  # Or any other appropriate view
    
    return response if response else redirect('websitetemplate')

    
class PurchasedView(ListView):
    template_name = 'web/purchased_templates.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        # Query payment models and retrieve corresponding templates/items
        paid_website_templates = Websitetemplate.objects.filter(id__in=Payment.objects.filter(user=user, payment_status='paid').values_list('template', flat=True))
        paid_mobile_templates = Mobiletemplate.objects.filter(id__in=PaymentMobiletemplate.objects.filter(user=user, payment_status='paid').values_list('mobiletemplate', flat=True))
        paid_desktop_templates = Desktoptemplate.objects.filter(id__in=PaymentDesktoptemplate.objects.filter(user=user, payment_status='paid').values_list('desktoptemplate', flat=True))
        paid_microsoft_templates = Microsofttemplate.objects.filter(id__in=PaymentMicrosofttemplate.objects.filter(user=user, payment_status='paid').values_list('microsofttemplate', flat=True))
        paid_adobe_templates = Adobetemplate.objects.filter(id__in=PaymentAdobetemplate.objects.filter(user=user, payment_status='paid').values_list('adobetemplate', flat=True))

        # Query other items similarly
        paid_websites = Website.objects.filter(id__in=PaymentWebsite.objects.filter(user=user, payment_status='paid').values_list('website', flat=True))
        paid_mobiles = Mobile.objects.filter(id__in=PaymentMobile.objects.filter(user=user, payment_status='paid').values_list('mobile', flat=True))
        paid_desktops = Desktop.objects.filter(id__in=PaymentDesktop.objects.filter(user=user, payment_status='paid').values_list('desktop', flat=True))
        paid_embededs = Embeded.objects.filter(id__in=PaymentEmbeded.objects.filter(user=user, payment_status='paid').values_list('embeded', flat=True))
        paid_graphics = Graphics.objects.filter(id__in=PaymentGraphics.objects.filter(user=user, payment_status='paid').values_list('graphics', flat=True))
        paid_projects = Project.objects.filter(id__in=PaymentProject.objects.filter(user=user, payment_status='paid').values_list('project', flat=True))
        paid_images = Image.objects.filter(id__in=PaymentImage.objects.filter(user=user, payment_status='paid').values_list('image', flat=True))
        
        
        # Query for digital product
        paid_book = Book.objects.filter(id__in=PaymentBook.objects.filter(user=user, payment_status='paid').values_list('book', flat=True))
        paid_printable = Printable.objects.filter(id__in=PaymentPrintable.objects.filter(user=user, payment_status='paid').values_list('product', flat=True))
        paid_music = Music.objects.filter(id__in=PaymentMusic.objects.filter(user=user, payment_status='paid').values_list('product', flat=True))
        paid_multimedia = Multimedia.objects.filter(id__in=PaymentMultimedia.objects.filter(user=user, payment_status='paid').values_list('product', flat=True))
        paid_digitalArt = DigitalArt.objects.filter(id__in=PaymentDigitalArt.objects.filter(user=user, payment_status='paid').values_list('product', flat=True))
        paid_CAD = CAD.objects.filter(id__in=PaymentCAD.objects.filter(user=user, payment_status='paid').values_list('product', flat=True))
        paid_software = Software.objects.filter(id__in=PaymentSoftware.objects.filter(user=user, payment_status='paid').values_list('product', flat=True))
        paid_business = Business.objects.filter(id__in=PaymentBusiness.objects.filter(user=user, payment_status='paid').values_list('product', flat=True))
        
        context = {
            'paid_website_templates': paid_website_templates,
            'paid_mobile_templates': paid_mobile_templates,
            'paid_desktop_templates': paid_desktop_templates,
            'paid_microsoft_templates': paid_microsoft_templates,
            'paid_adobe_templates': paid_adobe_templates,
            'paid_websites': paid_websites,
            'paid_mobiles': paid_mobiles,
            'paid_desktops': paid_desktops,
            'paid_embededs': paid_embededs,
            'paid_graphics': paid_graphics,
            'paid_projects': paid_projects,
            'paid_images': paid_images,
            
            'paid_book': paid_book,
            'paid_printable': paid_printable,
            'paid_music': paid_music,
            'paid_multimedia': paid_multimedia,
            'paid_digitalArt': paid_digitalArt,
            'paid_CAD': paid_CAD,
            'paid_software': paid_software,
            'paid_business': paid_business,
        }

        return render(request, self.template_name, context)

@disable_browser_cache
@transaction.atomic
def process_websitetemplate_purchase(request, template_id):
    user = request.user  # The user making the purchase (buyer)
    template = Websitetemplate.objects.get(id=template_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewwebsitetemplate', args=[template_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewwebsitetemplate', args=[template_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()
        
    request.session['amount'] = "0.00"
    return redirect(reverse('viewwebsitetemplate', args=[template_id]))
    
@transaction.atomic
def process_mobiletemplate_purchase(request, mobiletemplate_id):
    user = request.user  # The user making the purchase (buyer)
    template = Mobiletemplate.objects.get(id=mobiletemplate_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewmobiletemplate', args=[mobiletemplate_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewmobiletemplate', args=[mobiletemplate_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewmobiletemplate', args=[mobiletemplate_id]))

@never_cache
@transaction.atomic
def process_desktoptemplate_purchase(request, desktoptemplate_id):
    user = request.user  # The user making the purchase (buyer)
    template = Desktoptemplate.objects.get(id=desktoptemplate_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewdesktoptemplate', args=[desktoptemplate_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewdesktoptemplate', args=[desktoptemplate_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewdesktoptemplate', args=[desktoptemplate_id]))
    
@transaction.atomic
def process_microsofttemplate_purchase(request, microsofttemplate_id):
    user = request.user  # The user making the purchase (buyer)
    template = Microsofttemplate.objects.get(id=microsofttemplate_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewmicrosofttemplate', args=[microsofttemplate_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewmicrosofttemplate', args=[microsofttemplate_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewmicrosofttemplate', args=[microsofttemplate_id]))
    
@transaction.atomic
def process_adobetemplate_purchase(request, adobetemplate_id):
    user = request.user  # The user making the purchase (buyer)
    template = Adobetemplate.objects.get(id=adobetemplate_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewadobetemplate', args=[adobetemplate_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewadobetemplate', args=[adobetemplate_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewadobetemplate', args=[adobetemplate_id]))
    
@transaction.atomic
def process_website_purchase(request, course_id):
    user = request.user  # The user making the purchase (buyer)
    template = Website.objects.get(id=course_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewwebsite', args=[course_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewwebsite', args=[course_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session.pop('amount', None)
    
@transaction.atomic
def process_mobile_purchase(request, course_id):
    user = request.user  # The user making the purchase (buyer)
    template = Mobile.objects.get(id=course_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewmobile', args=[course_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewmobile', args=[course_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session.pop('amount', None)
    
@transaction.atomic
def process_desktop_purchase(request, course_id):
    user = request.user  # The user making the purchase (buyer)
    template = Desktop.objects.get(id=course_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewdesktop', args=[course_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewdesktop', args=[course_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session.pop('amount', None)
    
@transaction.atomic
def process_embeded_purchase(request, course_id):
    user = request.user  # The user making the purchase (buyer)
    template = Embeded.objects.get(id=course_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewembeded', args=[course_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewembeded', args=[course_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session.pop('amount', None)
    
@transaction.atomic
def process_graphics_purchase(request, course_id):
    user = request.user  # The user making the purchase (buyer)
    template = Graphics.objects.get(id=course_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewgraphics', args=[course_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewgraphics', args=[course_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session.pop('amount', None)
    
@transaction.atomic
def process_project_purchase(request, product_id):
    user = request.user  # The user making the purchase (buyer)
    template = Project.objects.get(id=product_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewproject', args=[product_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewproject', args=[product_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewproject', args=[product_id]))

# PROCESS DIGITAL PRODUCT PURCHASE
@transaction.atomic
def process_book_purchase(request, product_id):
    user = request.user  # The user making the purchase (buyer)
    template = Book.objects.get(id=product_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewbook', args=[product_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewbook', args=[product_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewbook', args=[product_id]))
    
@transaction.atomic
def process_printable_purchase(request, product_id):
    user = request.user  # The user making the purchase (buyer)
    template = Printable.objects.get(id=product_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewprintable', args=[product_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewprintable', args=[product_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewprintable', args=[product_id]))
    
@transaction.atomic
def process_music_purchase(request, product_id):
    user = request.user  # The user making the purchase (buyer)
    template = Music.objects.get(id=product_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewmusic', args=[product_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewmusic', args=[product_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewmusic', args=[product_id]))
    
@transaction.atomic
def process_multimedia_purchase(request, product_id):
    user = request.user  # The user making the purchase (buyer)
    template = Multimedia.objects.get(id=product_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewmultimedia', args=[product_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewmultimedia', args=[product_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewmultimedia', args=[product_id]))
    
@transaction.atomic
def process_digitalArt_purchase(request, product_id):
    user = request.user  # The user making the purchase (buyer)
    template = DigitalArt.objects.get(id=product_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewdigitalArt', args=[product_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewdigitalArt', args=[product_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewdigitalArt', args=[product_id]))
    
    
@transaction.atomic
def process_CAD_purchase(request, product_id):
    user = request.user  # The user making the purchase (buyer)
    template = CAD.objects.get(id=product_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewCAD', args=[product_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewCAD', args=[product_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewCAD', args=[product_id]))
    
@transaction.atomic
def process_software_purchase(request, product_id):
    user = request.user  # The user making the purchase (buyer)
    template = Software.objects.get(id=product_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewsoftware', args=[product_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewsoftware', args=[product_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewsoftware', args=[product_id]))
    
@transaction.atomic
def process_business_purchase(request, product_id):
    user = request.user  # The user making the purchase (buyer)
    template = Business.objects.get(id=product_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewbusiness', args=[product_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewbusiness', args=[product_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session['amount'] = "0.00"
    return redirect(reverse('viewbusiness', args=[product_id]))
    
    
@transaction.atomic
def process_image_purchase(request, product_id):
    user = request.user  # The user making the purchase (buyer)
    template = Image.objects.get(id=product_id)
    seller = template.user  # The user who owns the template (seller)
    
    # Retrieve the amount from session and ensure it's a Decimal
    amount = request.session.get('amount')
    
    if amount is None:
        # Handle case where amount is missing
        return redirect(reverse('viewimage', args=[product_id]))

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        # Handle case where amount cannot be converted to Decimal
        return redirect(reverse('viewimage', args=[product_id]))

    # Check if the seller has a Myamount record
    my_amount_record = Myamount.objects.filter(user=seller).first()
    masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
    
    if not my_amount_record:
        # If the record does not exist, create it
        my_amount_record = Myamount.objects.create(
            user=seller,
            Total_amount=amount,
            My_amount=Decimal(0.8) * amount,
            Reducted_amount=Decimal(0.2) * amount,
            Withdrawed_amount=Decimal('0.00')
        )
        if not masteramount:
            # If the record does not exist, create it
            masteramount = MasterAmount.objects.create(
            My_amount=Decimal(0.115) * amount,
            Gateway_Amount=Decimal(0.085) * amount,
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.My_amount += Decimal(0.115) * amount
            masteramount.Gateway_Amount=Decimal(0.085) * amount
            my_amount_record.save()
        request.session['amount'] = "0.00"
    else:
        # If the record exists, update it
        my_amount_record.Total_amount += amount
        my_amount_record.My_amount += Decimal(0.8) * amount
        my_amount_record.Reducted_amount=Decimal(0.2) * amount
        my_amount_record.save()
        
        masteramount.My_amount += Decimal(0.115) * amount
        masteramount.Gateway_Amount=Decimal(0.085) * amount
        my_amount_record.save()

    # Clear the session data if necessary
    request.session.pop('amount', None)
    return redirect(reverse('viewimage', args=[product_id]))
    
@login_required(login_url='signin')
def withdraw(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    cardinfo = Card.objects.filter(user=request.user).first()
    
    # Check if the user has a Myamount record; if not, create a default one
    my_amount_record = Myamount.objects.filter(user=request.user).first()
    
    if not my_amount_record:
        # Create a default Myamount record with 0.00 values
        my_amount_record = Myamount.objects.create(
            user=request.user,
            Total_amount=Decimal('0.00'),
            My_amount=Decimal('0.00'),
            Reducted_amount=Decimal('0.00'),
            Withdrawed_amount=Decimal('0.00')
        )

    withdraw = WithdrawForm()

    if request.method == "POST":
        withdraw = WithdrawForm(request.POST, files=request.FILES)
        
        if withdraw.is_valid():
            withdraw_instance = withdraw.save(commit=False)

            if my_amount_record.My_amount < withdraw_instance.Amount_in_USD:
                messages.info(request, 'Amount to withdraw is greater than your balance.')
            elif withdraw_instance.Amount_in_USD < 20:
                messages.info(request, 'Sorry! Minimum Amount To Withdraw is $20.')
            elif not cardinfo:
                messages.info(request, 'Please add your card details before making a withdrawal.')
                return redirect('mycard')
            else:
                # Update Myamount record with new values
                twent = withdraw_instance.Amount_in_USD * Decimal('0.25')
                my_amount_record.Total_amount -= (withdraw_instance.Amount_in_USD + twent)
                my_amount_record.My_amount -= withdraw_instance.Amount_in_USD
                my_amount_record.Reducted_amount -= twent
                my_amount_record.Withdrawed_amount += withdraw_instance.Amount_in_USD
                my_amount_record.save()

                # Save the withdraw record
                withdraw_instance.user = request.user
                withdraw_instance.Email = request.user.email
                
                withdraw_instance.Card_Number = cardinfo.Card_Number
                withdraw_instance.Card_Name = cardinfo.Card_Name
                withdraw_instance.Phone_Number = cardinfo.Phone_Number
                withdraw_instance.Country = cardinfo.Country
                withdraw_instance.Card_Type = cardinfo.Card_Type
                
                withdraw_instance.Status = 'Processing'
                withdraw_instance.save()
                
                fname = request.user.first_name
                lname = request.user.last_name
                email = request.user.email
                
                subject = "WORNTECH ONLINE SERVICES"
                message = f"Hellow {fname} {lname} You have withdrawed ${withdraw_instance.Amount_in_USD} from Worntech, you money will be confirmed soon, For any isue contact us, contact +255 710 891 288"
                #from_email = settings.EMAIL_HOST_USER
                from_email = 'worntechservices@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=True)

                messages.info(request, 'Money withdrawn successfully.')
                return redirect('withdraw')

    context = {
        "withdraw": withdraw,
        "cardinfo": cardinfo,
        'my_amount_record': my_amount_record,
        "notification": notification,
        'notificationcount': notificationcount,
    }
    
    return render(request, 'web/withdraw.html', context)

@login_required(login_url='signin')
def mycard(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    cardinfo = Card.objects.filter(user=request.user)
        
    mycard = CardForm()

    if request.method == "POST":
        mycard = CardForm(request.POST, files=request.FILES)

        if mycard.is_valid():
            mycard_instance = mycard.save(commit=False)

            # Add card information
            mycard_instance.user = request.user
            mycard_instance.First_Name = request.user.first_name
            mycard_instance.Last_Name = request.user.last_name
            mycard_instance.Email = request.user.email
            mycard.save()
                
            fname = request.user.first_name
            lname = request.user.last_name
            email = request.user.email
                
            subject = "WORNTECH ONLINE SERVICES"
            message = f"Hellow {fname} {lname} You have added {mycard_instance.Card_Number} in Worntech online services, Thanks, now you can cashout using this card, For any isue contact us, contact +255 710 891 288"
            #from_email = settings.EMAIL_HOST_USER
            from_email = 'worntechservices@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            messages.info(request, 'Card Added Successfully.')
            return redirect('mycard')

    context = {
        "mycard": mycard,
        "cardinfo": cardinfo,
        "notification": notification,
        'notificationcount': notificationcount,
    }
    
    return render(request, 'web/mycard.html', context)

@login_required(login_url='signin')
def cardinfo(request):
    
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    cardinfo = Card.objects.all()
    context = {
        'cardinfo': cardinfo,
        
        'notification': notification,
        'notificationcount': notificationcount,
    }
    return render(request, 'web/cardinfo.html', context)

@login_required(login_url='signin')
def master_withdraw(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    user_amount = Myamount.objects.aggregate(total=Sum('My_amount'))['total']
    masteramount = get_object_or_404(MasterAmount, unique_code='welcomemasterofus')
    
    
    masterwithdraw = MasterWithdrawForm()
    amount = MasterAmount.objects.filter(unique_code="welcomemasterofus").first()
    
    if user_amount is None:
            user_amount = Decimal('0.00')
    else:
        user_amount = round(user_amount, 2)
        
    total_amount = user_amount + masteramount.My_amount + masteramount.Gateway_Amount
    
    if request.method == "POST":
        masterwithdraw = MasterWithdrawForm(request.POST, files=request.FILES)
        amount = MasterAmount.objects.filter(unique_code="welcomemasterofus").first()
        
        if masterwithdraw.is_valid():
            masterwithdraw = masterwithdraw.save(commit=False)
            

            if (amount.My_amount < masterwithdraw.Amount_in_USD):
                messages.info(request, 'Amount to withdraw is greater than your balance.')
            else:
                
                # If the record exists, update it
                three = Decimal(masterwithdraw.Amount_in_USD) * Decimal('0.739')
                amount.My_amount -= masterwithdraw.Amount_in_USD
                amount.Gateway_Amount -= three
                amount.Withdrawed_amount += masterwithdraw.Amount_in_USD
                amount.save()
                
                masterwithdraw.user = request.user
                masterwithdraw.Email = request.user.email
                masterwithdraw.Status = 'Processing'
                masterwithdraw.save()
                messages.info(request, 'Money Withdrawed Succesefull.')
                return redirect('master_withdraw')

    context = {
        'user_amount': user_amount,
        'total_amount': total_amount,
        'masterwithdraw': masterwithdraw,
        'masteramount': masteramount,
        
        'notification': notification,
        'notificationcount': notificationcount,
    }
    return render(request, 'web/master_withdraw.html', context)

@login_required(login_url='signin')
def update_master_status(request, id, status):
    mypaymentview = get_object_or_404(MasterWithdraw, id=id)
    
    # Update the status based on the passed parameter
    if status in ['Completed', 'Processing', 'Declined']:
        mypaymentview.Status = status
        mypaymentview.save()

    return redirect('viewmasterpayment', id=id)  # Redirect back to the payment view


@login_required(login_url='signin')
def mypayment(request):
    
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    payment = Withdraw.objects.filter(user=request.user)
    context = {
        'payment': payment,
        
        'notification': notification,
        'notificationcount': notificationcount,
    }
    return render(request, 'web/mypayment.html', context)

@login_required(login_url='signin')
def viewmypayment(request, id):
    
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    mypaymentview = Withdraw.objects.get(id=id)
    
    system_fee = 0.1438 * float(mypaymentview.Amount_in_USD)
    gateway_fee = 0.1063 * float(mypaymentview.Amount_in_USD)
    receiving = float(mypaymentview.Amount_in_USD)
    Total_amount = system_fee + gateway_fee + receiving
    
    context = {
        "mypaymentview":mypaymentview,
        "system_fee":system_fee,
        "gateway_fee":gateway_fee,
        "Total_amount":Total_amount,
        
        "notification":notification,
        "notificationcount":notificationcount,
        }
    return render(request, 'web/viewmypayment.html', context)

@login_required(login_url='signin')
def update_status(request, id, status):
    mypaymentview = get_object_or_404(Withdraw, id=id)
    
    # Update the status based on the passed parameter
    if status in ['Completed', 'Processing', 'Declined']:
        mypaymentview.Status = status
        mypaymentview.save()
        
        # Create a notification for the user
        message = ""
        if status == 'Completed':
            message = f"Confirmed you have received ${mypaymentview.Amount_in_USD} in card number {mypaymentview.Card_Number}, if there is any problem please contact us through whatsapp number +255 710891288, thank you for chosing worntech to sell your product."
        elif status == 'Processing':
            message = f"Withdraw of ${mypaymentview.Amount_in_USD} in card number {mypaymentview.Card_Number} is in process plese wait for the confirmation, if there is any problem please contact us through whatsapp number +255 710891288, thank you for chosing worntech to sell your product."
        elif status == 'Declined':
            message = f"Withdraw of ${mypaymentview.Amount_in_USD} in card number {mypaymentview.Card_Number} is declained, if there is any problem please contact us through whatsapp number +255 710891288, thank you for chosing worntech to sell your product."

        # Assuming the user is the one making the request
        Notification.objects.create(
            user=mypaymentview.user,  # Replace with appropriate user if needed
            message=message,
            status=status
        )

    return redirect('viewmypayment', id=id)  # Redirect back to the payment view


def view_notifications(request, id):
    notifications = Notification.objects.get(id=id)
    
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    # Mark the notification as viewed
    notifications.viewed = True
    notifications.save()  # Save the change to the database

    context = {
        'notifications': notifications,
        'notification': notification,
        'notificationcount': notificationcount,
    }
    
    return render(request, 'web/view_notifications.html', context)


def delete_viewed_notifications(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, viewed=True).delete()
        return JsonResponse({"message": "Notifications deleted successfully"}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required(login_url='signin')
def allpayment(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    payment = Withdraw.objects.all()
    context = {
        'payment': payment,
        
        'notification': notification,
        'notificationcount': notificationcount,
    }
    return render(request, 'web/allpayment.html', context)

@login_required(login_url='signin')
def masterpayment(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    payment = MasterWithdraw.objects.all()
    context = {
        'payment': payment,
        
        'notification': notification,
        'notificationcount': notificationcount,
    }
    return render(request, 'web/masterpayment.html', context)

@login_required(login_url='signin')
def viewmasterpayment(request, id):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    mypaymentview = MasterWithdraw.objects.get(id=id)
    
    # system_fee = 0.2125 * float(mypaymentview.Amount_in_USD)
    gateway_fee = 0.739 * float(mypaymentview.Amount_in_USD)
    receiving = float(mypaymentview.Amount_in_USD)
    Total_amount = gateway_fee + receiving
    
    context = {
        "mypaymentview":mypaymentview,
        "gateway_fee":gateway_fee,
        "Total_amount":Total_amount,
        
        "notification":notification,
        "notificationcount":notificationcount,
        }
    return render(request, 'web/viewmasterpayment.html', context)

def completed_transaction(request):
    payment = Payment.objects.all()
    paymentmobiletemplate = PaymentMobiletemplate.objects.all()
    paymentdesktoptemplate = PaymentDesktoptemplate.objects.all()
    paymentmicrosofttemplate = PaymentMicrosofttemplate.objects.all()
    paymentadobetemplate = PaymentAdobetemplate.objects.all()
    paymentwebsite = PaymentWebsite.objects.all()
    paymentmobile = PaymentMobile.objects.all()
    paymentdesktop = PaymentDesktop.objects.all()
    paymentembeded = PaymentEmbeded.objects.all()
    paymentgraphics = PaymentGraphics.objects.all()
    paymentproject = PaymentProject.objects.all()
    paymentimage = PaymentImage.objects.all()
    
    
    paymentbook = PaymentBook.objects.all()
    paymentprintable = PaymentPrintable.objects.all()
    paymentmusic = PaymentMusic.objects.all()
    paymentmultimedia = PaymentMultimedia.objects.all()
    paymentdigitalArt = PaymentDigitalArt.objects.all()
    paymentCAD = PaymentCAD.objects.all()
    paymentsoftware = PaymentSoftware.objects.all()
    paymentbusiness = PaymentBusiness.objects.all()
    
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    context = {
        'payment': payment,
        'paymentmobiletemplate': paymentmobiletemplate,
        'paymentdesktoptemplate': paymentdesktoptemplate,
        'paymentmicrosofttemplate': paymentmicrosofttemplate,
        'paymentadobetemplate': paymentadobetemplate,
        'paymentwebsite': paymentwebsite,
        'paymentmobile': paymentmobile,
        'paymentdesktop': paymentdesktop,
        'paymentembeded': paymentembeded,
        'paymentgraphics': paymentgraphics,
        'paymentproject': paymentproject,
        'paymentimage': paymentimage,
        
        'paymentbook': paymentbook,
        'paymentprintable': paymentprintable,
        'paymentmusic': paymentmusic,
        'paymentmultimedia': paymentmultimedia,
        'paymentdigitalArt': paymentdigitalArt,
        'paymentCAD': paymentCAD,
        'paymentsoftware': paymentsoftware,
        'paymentbusiness': paymentbusiness,
        
        'notification': notification,
        'notificationcount': notificationcount,
    }
    return render(request, 'web/completed_transaction.html', context)

def pending_transaction(request):
    payment = Payment.objects.all()
    paymentmobiletemplate = PaymentMobiletemplate.objects.all()
    paymentdesktoptemplate = PaymentDesktoptemplate.objects.all()
    paymentmicrosofttemplate = PaymentMicrosofttemplate.objects.all()
    paymentadobetemplate = PaymentAdobetemplate.objects.all()
    paymentwebsite = PaymentWebsite.objects.all()
    paymentmobile = PaymentMobile.objects.all()
    paymentdesktop = PaymentDesktop.objects.all()
    paymentembeded = PaymentEmbeded.objects.all()
    paymentgraphics = PaymentGraphics.objects.all()
    paymentproject = PaymentProject.objects.all()
    paymentimage = PaymentImage.objects.all()
    
    paymentbook = PaymentBook.objects.all()
    paymentprintable = PaymentPrintable.objects.all()
    paymentmusic = PaymentMusic.objects.all()
    paymentmultimedia = PaymentMultimedia.objects.all()
    paymentdigitalArt = PaymentDigitalArt.objects.all()
    paymentCAD = PaymentCAD.objects.all()
    paymentsoftware = PaymentSoftware.objects.all()
    paymentbusiness = PaymentBusiness.objects.all()
    
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    context = {
        'payment': payment,
        'paymentmobiletemplate': paymentmobiletemplate,
        'paymentdesktoptemplate': paymentdesktoptemplate,   
        'paymentmicrosofttemplate': paymentmicrosofttemplate,
        'paymentadobetemplate': paymentadobetemplate,
        'paymentwebsite': paymentwebsite,
        'paymentmobile': paymentmobile,
        'paymentdesktop': paymentdesktop,
        'paymentembeded': paymentembeded,
        'paymentgraphics': paymentgraphics,
        'paymentproject': paymentproject,
        'paymentimage': paymentimage,
        
        'paymentbook': paymentbook,
        'paymentprintable': paymentprintable,
        'paymentmusic': paymentmusic,
        'paymentmultimedia': paymentmultimedia,
        'paymentdigitalArt': paymentdigitalArt,
        'paymentCAD': paymentCAD,
        'paymentsoftware': paymentsoftware,
        'paymentbusiness': paymentbusiness,
        
        'notification': notification,
        'notificationcount': notificationcount,
    }
    return render(request, 'web/pending_transaction.html', context)

def failed_transaction(request):
    payment = Payment.objects.all()
    paymentmobiletemplate = PaymentMobiletemplate.objects.all()
    paymentdesktoptemplate = PaymentDesktoptemplate.objects.all()
    paymentmicrosofttemplate = PaymentMicrosofttemplate.objects.all()
    paymentadobetemplate = PaymentAdobetemplate.objects.all()
    paymentwebsite = PaymentWebsite.objects.all()
    paymentmobile = PaymentMobile.objects.all()
    paymentdesktop = PaymentDesktop.objects.all()
    paymentembeded = PaymentEmbeded.objects.all()
    paymentgraphics = PaymentGraphics.objects.all()
    paymentproject = PaymentProject.objects.all()
    paymentimage = PaymentImage.objects.all()
    
    paymentbook = PaymentBook.objects.all()
    paymentprintable = PaymentPrintable.objects.all()
    paymentmusic = PaymentMusic.objects.all()
    paymentmultimedia = PaymentMultimedia.objects.all()
    paymentdigitalArt = PaymentDigitalArt.objects.all()
    paymentCAD = PaymentCAD.objects.all()
    paymentsoftware = PaymentSoftware.objects.all()
    paymentbusiness = PaymentBusiness.objects.all()
    
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    context = {
        'payment': payment,
        'paymentmobiletemplate': paymentmobiletemplate,
        'paymentdesktoptemplate': paymentdesktoptemplate,
        'paymentmicrosofttemplate': paymentmicrosofttemplate,
        'paymentadobetemplate': paymentadobetemplate,
        'paymentwebsite': paymentwebsite,
        'paymentmobile': paymentmobile,
        'paymentdesktop': paymentdesktop,
        'paymentembeded': paymentembeded,
        'paymentgraphics': paymentgraphics,
        'paymentproject': paymentproject,
        'paymentimage': paymentimage,
        
        'paymentbook': paymentbook,
        'paymentprintable': paymentprintable,
        'paymentmusic': paymentmusic,
        'paymentmultimedia': paymentmultimedia,
        'paymentdigitalArt': paymentdigitalArt,
        'paymentCAD': paymentCAD,
        'paymentsoftware': paymentsoftware,
        'paymentbusiness': paymentbusiness,
        
        'notification': notification,
        'notificationcount': notificationcount,
    }
    return render(request, 'web/failed_transaction.html', context)

def my_transaction(request):
    payment = Payment.objects.filter(user=request.user)
    paymentmobiletemplate = PaymentMobiletemplate.objects.filter(user=request.user)
    paymentdesktoptemplate = PaymentDesktoptemplate.objects.filter(user=request.user)
    paymentmicrosofttemplate = PaymentMicrosofttemplate.objects.filter(user=request.user)
    paymentadobetemplate = PaymentAdobetemplate.objects.filter(user=request.user)
    paymentwebsite = PaymentWebsite.objects.filter(user=request.user)
    paymentmobile = PaymentMobile.objects.filter(user=request.user)
    paymentdesktop = PaymentDesktop.objects.filter(user=request.user)
    paymentembeded = PaymentEmbeded.objects.filter(user=request.user)
    paymentgraphics = PaymentGraphics.objects.filter(user=request.user)
    paymentproject = PaymentProject.objects.filter(user=request.user)
    paymentimage = PaymentImage.objects.filter(user=request.user)
    
    paymentbook = PaymentBook.objects.filter(user=request.user)
    paymentprintable = PaymentPrintable.objects.filter(user=request.user)
    paymentmusic = PaymentMusic.objects.filter(user=request.user)
    paymentmultimedia = PaymentMultimedia.objects.filter(user=request.user)
    paymentdigitalArt = PaymentDigitalArt.objects.filter(user=request.user)
    paymentCAD = PaymentCAD.objects.filter(user=request.user)
    paymentsoftware = PaymentSoftware.objects.filter(user=request.user)
    paymentbusiness = PaymentBusiness.objects.filter(user=request.user)
    
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    context = {
        'payment': payment,
        'paymentmobiletemplate': paymentmobiletemplate,
        'paymentdesktoptemplate': paymentdesktoptemplate,
        'paymentmicrosofttemplate': paymentmicrosofttemplate,
        'paymentadobetemplate': paymentadobetemplate,
        'paymentwebsite': paymentwebsite,
        'paymentmobile': paymentmobile,
        'paymentdesktop': paymentdesktop,
        'paymentembeded': paymentembeded,
        'paymentgraphics': paymentgraphics,
        'paymentproject': paymentproject,
        'paymentimage': paymentimage,
        
        'paymentbook': paymentbook,
        'paymentprintable': paymentprintable,
        'paymentmusic': paymentmusic,
        'paymentmultimedia': paymentmultimedia,
        'paymentdigitalArt': paymentdigitalArt,
        'paymentCAD': paymentCAD,
        'paymentsoftware': paymentsoftware,
        'paymentbusiness': paymentbusiness,
        
        'notification': notification,
        'notificationcount': notificationcount,
    }
    return render(request, 'web/my_transaction.html', context)

@login_required(login_url='signin')
def allusers(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    alluser = MyUser.objects.all()
    
    context = {
        "alluser":alluser,
        
        "notification":notification,
        "notificationcount":notificationcount,
        }
    return render(request, 'web/allusers.html', context)

@login_required(login_url='signin')
def staffusers(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    staffuser = MyUser.objects.all()
    
    context = {
        "staffuser":staffuser,
        
        "notification":notification,
        "notificationcount":notificationcount,
        }
    return render(request, 'web/staffusers.html', context)

@login_required(login_url='signin')
def adminusers(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    adminuser = MyUser.objects.all()
    
    context = {
        "adminuser":adminuser,
        
        "notification":notification,
        "notificationcount":notificationcount,
        }
    return render(request, 'web/adminusers.html', context)

@login_required(login_url='signin')
def useramount(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    amount = Myamount.objects.all()
    
    context = {
        "amount":amount,
        
        "notification":notification,
        "notificationcount":notificationcount,
        }
    return render(request, 'web/useramount.html', context)

def help(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    context = {
        "notification":notification,
        "notificationcount":notificationcount,
        }
    
    return render(request, 'web/help.html', context)
def terms_conditions(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    context = {
        "notification":notification,
        "notificationcount":notificationcount,
        }
    
    return render(request, 'web/terms_conditions.html', context)





# SEARCHING VIEWS
def search_all_product(request):
    query = request.GET.get('q')

    if query:
        # Split the query into individual words
        query_words = query.split()

        # Construct a query that looks for each word in the Title
        queries = Q()
        for word in query_words:
            queries |= Q(Title__icontains=word)

        # Filter templates that match any of the query words
        productproject = Project.objects.filter(queries)
        productimage = Image.objects.filter(queries)
        productbook = Book.objects.filter(queries)
        productprintable = Printable.objects.filter(queries)
        productmusic = Music.objects.filter(queries)
        productmultmedia = Multimedia.objects.filter(queries)
        productdigitalart = DigitalArt.objects.filter(queries)
        productcad = CAD.objects.filter(queries)
        productsoftware = Software.objects.filter(queries)
        productbusiness = Business.objects.filter(queries)
        productwebsitetemplate = Websitetemplate.objects.filter(queries)
        productmobiletemplate = Mobiletemplate.objects.filter(queries)
        productdesktoptemplate = Desktoptemplate.objects.filter(queries)
        productmirosofttemplate = Microsofttemplate.objects.filter(queries)
        productadobetemplate = Adobetemplate.objects.filter(queries)
    else:
        productproject = Project.objects.all()
        productimage = Image.objects.all()
        productbook = Book.objects.all()
        productprintable = Printable.objects.all()
        productmusic = Music.objects.all()
        productmultmedia = Multimedia.objects.all()
        productdigitalart = DigitalArt.objects.all()
        productcad = CAD.objects.all()
        productsoftware = Software.objects.all()
        productbusiness = Business.objects.all()
        productwebsitetemplate = Websitetemplate.objects.all()
        productmobiletemplate = Mobiletemplate.objects.all()
        productdesktoptemplate = Desktoptemplate.objects.all()
        productmirosofttemplate = Microsofttemplate.objects.all()
        productadobetemplate = Adobetemplate.objects.all()
        
    # Prepare data for each template
    for template in productproject:
        avg_rating = ReviewProject.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewProject.objects.filter(template=template).count()  # Total reviews
        
    for template in productimage:
        avg_rating = ReviewImage.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewImage.objects.filter(template=template).count()  # Total reviews
        
    for template in productbook:
        avg_rating = ReviewBook.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBook.objects.filter(template=template).count()  # Total reviews
        
    for template in productprintable:
        avg_rating = ReviewPrintable.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewPrintable.objects.filter(template=template).count()  # Total reviews
        
    for template in productmusic:
        avg_rating = ReviewMusic.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMusic.objects.filter(template=template).count()  # Total reviews
        
    for template in productmultmedia:
        avg_rating = ReviewMultimedia.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMultimedia.objects.filter(template=template).count()  # Total reviews
        
    for template in productdigitalart:
        avg_rating = ReviewDigitalArt.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDigitalArt.objects.filter(template=template).count()  # Total reviews
        
    for template in productcad:
        avg_rating = ReviewCAD.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewCAD.objects.filter(template=template).count()  # Total reviews
        
    for template in productsoftware:
        avg_rating = ReviewSoftware.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewSoftware.objects.filter(template=template).count()  # Total reviews
        
    for template in productbusiness:
        avg_rating = ReviewBusiness.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewBusiness.objects.filter(template=template).count()  # Total reviews
        
    for template in productwebsitetemplate:
        avg_rating = ReviewWebsitetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewWebsitetemplate.objects.filter(template=template).count()  # Total reviews
        
    for template in productmobiletemplate:
        avg_rating = ReviewMobiletemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMobiletemplate.objects.filter(template=template).count()  # Total reviews
        
    for template in productdesktoptemplate:
        avg_rating = ReviewDesktoptemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewDesktoptemplate.objects.filter(template=template).count()  # Total reviews
        
    for template in productmirosofttemplate:
        avg_rating = ReviewMicrosofttemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewMicrosofttemplate.objects.filter(template=template).count()  # Total reviews
        
    for template in productadobetemplate:
        avg_rating = ReviewAdobetemplate.objects.filter(template=template).aggregate(Avg('rating'))['rating__avg'] or 0
        template.avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        template.total_reviews = ReviewAdobetemplate.objects.filter(template=template).count()  # Total reviews
    
    # Create context outside the if-else
    context = {
        'productproject': productproject,
        'productimage': productimage,
        'productbook': productbook,
        'productprintable': productprintable,
        'productmusic': productmusic,
        'productmultmedia': productmultmedia,
        'productdigitalart': productdigitalart,
        'productcad': productcad,
        'productsoftware': productsoftware,
        'productbusiness': productbusiness,
        'productwebsitetemplate': productwebsitetemplate,
        'productmobiletemplate': productmobiletemplate,
        'productdesktoptemplate': productdesktoptemplate,
        'productmirosofttemplate': productmirosofttemplate,
        'productadobetemplate': productadobetemplate,
    }

    return render(request, 'web/allproduct.html', context)


# FOR SUBSCRIBERS
def subscription(request):
    subscription = Subscription.objects.all()
    
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    context={
        "subscription":subscription,
        "notification":notification,
        "notificationcount":notificationcount,
    }
    return render(request, 'web/subscription.html',context)

def successsubscription(request):
    return render(request, 'web/successsubscription.html')

