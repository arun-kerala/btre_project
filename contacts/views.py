from django.shortcuts import redirect, render
from . models import Contact
from django.contrib import messages
from django.core.mail import send_mail


# Create your views here.
def contact(request):
   if request.method == "POST":
      listing_id = request.POST['listing_id']
      listing = request.POST['listing']
      name = request.POST['name']
      email = request.POST['email']
      phone = request.POST['phone']
      message = request.POST['message']
      user_id = request.POST['user_id']
      realtor_email = request.POST['realtor_email']

      # check if user has made inquiry already
      if request.user.is_authenticated:
         user_id = request.user.id
         has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
         if has_contacted:
            messages.error(request,'you have already made an inquiry on this listing')
            return redirect('/listings/'+listing_id)

      contact = Contact(listing=listing,listing_id=listing_id,name=name,email=email,phone=phone,message=message,user_id=user_id)
      contact.save()

      # send email
      send_mail(
         'Property listing inquiry',
         'There has been an inquiry for'+listing,
         'from@example.com',
         ['to@example.com'],
         fail_silently=False

      )

      messages.success(request,'your request has been submitted, a realtor will get back to you soon')
      return redirect('/listings/'+listing_id)
