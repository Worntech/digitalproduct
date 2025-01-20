from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class MyUserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'username']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['Full_Name', 'Subject', 'Email', 'Phone', 'Message']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']

     #for website
class WebsiteForm(ModelForm):
    class Meta:
        model = Website
        fields = ['Title', 'Course', 'Part', 'Explanation', 'Image', 'Video', 'amount_in_USD']

    #for comment of the website
class CommentwebsiteForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentwebsite
        fields = ('content',)
        
    #for mobile
class MobileForm(ModelForm):
    class Meta:
        model = Mobile
        fields = ['Title', 'Course', 'Part', 'Explanation', 'Image', 'Video', 'amount_in_USD']
        
#for comment of the mobile
class CommentmobileForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentmobile
        fields = ('content',)
        
    #for desktop
class DesktopForm(ModelForm):
    class Meta:
        model = Desktop
        fields = ['Title', 'Course', 'Explanation', 'Image', 'Video', 'amount_in_USD']
        
#for comment of the desktop
class CommentdesktopForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentdesktop
        fields = ('content',)
        
    #for embeded
class EmbededForm(ModelForm):
    class Meta:
        model = Embeded
        fields = ['Title', 'Course', 'Explanation', 'Image', 'Video', 'amount_in_USD']
        
#for comment of the embeded
class CommentembededForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentembeded
        fields = ('content',)
        
#for embeded
class GraphicsForm(ModelForm):
    class Meta:
        model = Graphics
        fields = ['Title', 'Course', 'Explanation', 'Image', 'Video', 'amount_in_USD']
   
   #for comment of the graphics
class CommentgraphicsForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentgraphics
        fields = ('content',)
             
# FOR PROJECT MODEL
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['Title', 'Explanation', 'Type', 'Image', 'Preview_Video', 'Project', 'amount_in_USD']
        
class ReviewProjectForm(forms.ModelForm):
    class Meta:
        model = ReviewProject
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }       
        
#for comment of the project
class CommentprojectForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentproject
        fields = ('content',)
        
# FOR IMAGE MODEL
class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['Title', 'Image', 'Image_download', 'amount_in_USD']
        
class ReviewImageForm(forms.ModelForm):
    class Meta:
        model = ReviewImage
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
            
#for comment of the project
class CommentimageForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentimage
        fields = ('content',)
        
#for website template
class WebsitetemplateForm(ModelForm):
    class Meta:
        model = Websitetemplate
        fields = ['Title', 'Type', 'Explanation', 'Image', 'Preview_Video', 'Template', 'amount_in_USD', 'preview']

class ReviewWebsitetemplateForm(forms.ModelForm):
    class Meta:
        model = ReviewWebsitetemplate
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
        
    #for mobile template
class MobiletetemplateForm(ModelForm):
    class Meta:
        model = Mobiletemplate
        fields = ['Title', 'Type', 'Explanation', 'Image', 'Preview_Video', 'Template', 'amount_in_USD']

class ReviewMobiletemplateForm(forms.ModelForm):
    class Meta:
        model = ReviewMobiletemplate
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
        
              
    #for desktop template
class DesktoptemplateForm(ModelForm):
    class Meta:
        model = Desktoptemplate
        fields = ['Title', 'Type', 'Explanation', 'Image', 'Preview_Video', 'Template', 'amount_in_USD']

class ReviewDesktoptemplateForm(forms.ModelForm):
    class Meta:
        model = ReviewDesktoptemplate
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
              
    #for microspft template
class MicrosofttemplateForm(ModelForm):
    class Meta:
        model = Microsofttemplate
        fields = ['Title', 'Type', 'Explanation', 'Image', 'Preview_Video', 'Template', 'amount_in_USD']

class ReviewMicrosofttemplateForm(forms.ModelForm):
    class Meta:
        model = ReviewMicrosofttemplate
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
               
    #for adobe tempalte
class AdobetemplateForm(ModelForm):
    class Meta:
        model = Adobetemplate
        fields = ['Title', 'Type', 'Explanation', 'Image', 'Preview_Video', 'Template', 'amount_in_USD']

class ReviewAdobetemplateForm(forms.ModelForm):
    class Meta:
        model = ReviewAdobetemplate
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }       
     
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['Title', 'Category', 'Explanation', 'Image', 'Book', 'amount_in_USD']

class ReviewBookForm(forms.ModelForm):
    class Meta:
        model = ReviewBook
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
        
class CommentbookForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentbook
        fields = ('content',)
        
               
class PrintableForm(ModelForm):
    class Meta:
        model = Printable
        fields = ['Title', 'Category', 'Explanation', 'Image', 'Product', 'amount_in_USD']

class ReviewPrintableForm(forms.ModelForm):
    class Meta:
        model = ReviewPrintable
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
        
class CommentprintableForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentprintable
        fields = ('content',)
        
             
class MusicForm(ModelForm):
    class Meta:
        model = Music
        fields = ['Title', 'Category', 'Explanation', 'Image', 'Product', 'Preview_Audio', 'amount_in_USD']

class ReviewMusicForm(forms.ModelForm):
    class Meta:
        model = ReviewMusic
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
        
class CommentmusicForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentmusic
        fields = ('content',)
        
           
class MultimediaForm(ModelForm):
    class Meta:
        model = Multimedia
        fields = ['Title', 'Category', 'Explanation', 'Image', 'Preview_Video', 'Product', 'amount_in_USD']


class ReviewMultimediaForm(forms.ModelForm):
    class Meta:
        model = ReviewMultimedia
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
        
class CommentmultimediaForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentmultimedia
        fields = ('content',)
        
               
class DigitalArtForm(ModelForm):
    class Meta:
        model = DigitalArt
        fields = ['Title', 'Category', 'Explanation', 'Image', 'Preview_Video', 'Product', 'amount_in_USD']


class ReviewDigitalArtForm(forms.ModelForm):
    class Meta:
        model = ReviewDigitalArt
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
        
class CommentdigitalArtForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = CommentdigitalArt
        fields = ('content',)
        
          
class CADForm(ModelForm):
    class Meta:
        model = CAD
        fields = ['Title', 'Category', 'Explanation', 'Image', 'Preview_Video', 'Product', 'amount_in_USD']


class ReviewCADForm(forms.ModelForm):
    class Meta:
        model = ReviewCAD
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
        
class CommentCADForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = CommentCAD
        fields = ('content',)
        
              
class SoftwareForm(ModelForm):
    class Meta:
        model = Software
        fields = ['Title', 'Category', 'Explanation', 'Image', 'Preview_Video', 'Product', 'amount_in_USD']

class ReviewSoftwareForm(forms.ModelForm):
    class Meta:
        model = ReviewSoftware
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
        
class CommentsoftwareForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentsoftware
        fields = ('content',)
        
class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = ['Title', 'Category', 'Explanation', 'Image', 'Preview_Video', 'Product', 'amount_in_USD']

class ReviewBusinessForm(forms.ModelForm):
    class Meta:
        model = ReviewBusiness
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
        }
        
class CommentbusinessForm(forms.ModelForm):
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={

            'rows': '4',
            'id': 'content',
            'placeholder' : 'Write your Comment Here',
        }))
    class Meta:
        model = Commentbusiness
        fields = ('content',)
        
        
# PAYMENT MODEL
class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        
class PaymentMobiletemplateForm(ModelForm):
    class Meta:
        model = PaymentMobiletemplate
        fields = '__all__'
        
class PaymentDesktoptemplateForm(ModelForm):
    class Meta:
        model = PaymentDesktoptemplate
        fields = '__all__'


class PaymentMicrosofttemplateForm(ModelForm):
    class Meta:
        model = PaymentMicrosofttemplate
        fields = '__all__'
        
class PaymentAdobetemplateForm(ModelForm):
    class Meta:
        model = PaymentAdobetemplate
        fields = '__all__'
        
# PAYMENT MODEL FOR COURSES
class PaymentWebsiteForm(ModelForm):
    class Meta:
        model = PaymentWebsite
        fields = []
        
class PaymentMobileForm(ModelForm):
    class Meta:
        model = PaymentMobile
        fields = []
        
class PaymentDesktopForm(ModelForm):
    class Meta:
        model = PaymentDesktop
        fields = []


class PaymentEmbededForm(ModelForm):
    class Meta:
        model = PaymentEmbeded
        fields = []
        
class PaymentGraphicsForm(ModelForm):
    class Meta:
        model = PaymentGraphics
        fields = []

# PAYMENT OF PROJECT
class PaymentProjectForm(ModelForm):
    class Meta:
        model = PaymentProject
        fields = []
        
        
        
class PaymentBookForm(ModelForm):
    class Meta:
        model = PaymentBook
        fields = []
        
class PaymentPrintableForm(ModelForm):
    class Meta:
        model = PaymentPrintable
        fields = []
        
class PaymentMusicForm(ModelForm):
    class Meta:
        model = PaymentMusic
        fields = []
        
class PaymentMultimediaForm(ModelForm):
    class Meta:
        model = PaymentMultimedia
        fields = []
        
class PaymentDigitalArtForm(ModelForm):
    class Meta:
        model = PaymentDigitalArt
        fields = []
        
class PaymentCADForm(ModelForm):
    class Meta:
        model = PaymentCAD
        fields = []
        
class PaymentSoftwareForm(ModelForm):
    class Meta:
        model = PaymentSoftware
        fields = []
        
class PaymentBusinessForm(ModelForm):
    class Meta:
        model = PaymentBusiness
        fields = []

# PAYMENT OF PROJECT
class PaymentImageForm(ModelForm):
    class Meta:
        model = PaymentImage
        fields = []
        
# MY AMOUNT
class MyamountForm(ModelForm):
    class Meta:
        model = Myamount
        fields = []
        
# WITHDRAW
class WithdrawForm(ModelForm):
    class Meta:
        model = Withdraw
        fields = ['Amount_in_USD']
        
# MASTER WITHDRAW
class MasterWithdrawForm(ModelForm):
    class Meta:
        model = MasterWithdraw
        fields = ['Card_Number', 'Card_Name', 'Amount_in_USD', 'Phone_Number', 'Country']
        
# MASTER WITHDRAW
class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['Card_Number', 'Card_Name', 'Phone_Number', 'Card_Type', 'Country']


# MY MASTER AMOUNT
class MasterAmountForm(ModelForm):
    class Meta:
        model = MasterAmount
        fields = []
        
# NOTIFICATION
class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = []
