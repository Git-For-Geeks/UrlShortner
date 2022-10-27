from base64 import urlsafe_b64decode

from multiprocessing import *

from telnetlib import LOGOUT
from typing import Type
from datetime import datetime
from .models import ShortLongUrlStore

from django.conf import settings
from django.forms import EmailField, PasswordInput
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,send_mail

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str

from myproject import settings

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello World!")

def home_page(request):
    context = {
            "submitted" : False,
            "keyError" : False
        }
    if request.method == 'POST':
        # print(request.POST)
        data = request.POST #dict
        long_url = data.get('longurl')
        custom_name = data.get('custom_name')
        username = request.user.username
        
    
        
        try:
            #saving data to data base 
            #create
            obj=ShortLongUrlStore(long_url = long_url,short_url = custom_name,username=username) # table column name <- variable name
            obj.save()
            #read        
            date = obj.date #accessing date from database
            clicks = obj.clicks      
            context['long_url'] = long_url
            context['short_url'] = request.build_absolute_uri() + custom_name
            context['Date'] = date #taken from database
            # context['Date'] = datetime.now().strftime("%B %d, %Y %H : %M") # : %S") #using python
            context['Clicks'] = clicks
            context['submitted'] = True
            if request.user.is_authenticated:
                f_name=request.user.first_name
                context['fname']=f_name
        except:
            context['keyError'] = True
    else:
        print("User not sending any data")
        
    
    # print(request.method)
    return render(request,"index.html",context)

def redirect_url(request,DBreqCustomName):
    filterUrl = ShortLongUrlStore.objects.filter(short_url=DBreqCustomName)
    if len(filterUrl) == 0:
        return HttpResponse("No such short url found.")
    else:
        objFound=filterUrl[0]
        FoundLongUrl = objFound.long_url
        objFound.clicks = objFound.clicks + 1
        objFound.save()
        return redirect(FoundLongUrl)
    
def all_analytics(request):
    user = request.user
    rows = ShortLongUrlStore.objects.filter(username = user)
    context = {
        "rows" : rows
    }
    return render(request, "all-analytics.html",context)

def sign_up(request):
    if request.method == 'POST':
        # print(request.POST)
        data = request.POST #dict
        usernameIn=data.get('username')
        EmailIn = data.get('email')
        fnameIn=data.get('fname')
        lnameIn=data.get('lname')
        PswrdIn = data.get('pswrd')
        ConfirmPswrdIn = data.get('confirmpswrd')
        
        if User.objects.filter(username=usernameIn):
            messages.error(request,"Username already exists...Try another Username")
            return redirect('signup')

        if User.objects.filter(email=EmailIn):
            messages.error(request,"Email already registered...Try another email")
            return redirect('signup')
            
        if len(usernameIn)>10:
            messages.error(request,"Length of Username is > 10")
            return redirect('signup')
        
        if not usernameIn.isalnum():
            messages.error(request,"Only AlphaNumeric values are allowed as Username.")
            return redirect('signup')
        
        try:
            if (PswrdIn == ConfirmPswrdIn):
                myUser=User.objects.create_user(usernameIn,EmailIn,PswrdIn)
                myUser.first_name=fnameIn
                myUser.last_name = lnameIn
                myUser.is_active = True
                # myUser.is_active = False
                myUser.save()
                
                messages.success(request, "Your account is successfully created.Please login with your respective credentials")
            
                return redirect('signin')
                # return redirect('home')
            else:
                messages.error(request,"Password Mismatch")
        except:
            messages.error(request,"User Already exists...Plese Sign In to continue")
            return redirect('signin')
        
    return render(request,"signUp.html")

def sign_in(request):
    if request.method == 'POST':
        # print(request.POST)
        data = request.POST #dict
        username_emailChk=data.get('username_email')
        PswrdChk = data.get('pswrd')
        
        if '@' in username_emailChk:
            user = authenticate(email=username_emailChk,password=PswrdChk)
        else:
            user = authenticate(username=username_emailChk,password=PswrdChk)

            
        if user is not None:
            login(request,user)
            fname =  user.first_name
            context={
                'fname':fname,
            }
            return redirect('home')
            # return render(request,"index.html",context)
        else:
            messages.error(request,"Bad credentials")
            return redirect('signin')
    return render(request,"signIn.html")


def sign_out(request):
    logout(request)
    messages.success(request,"Successfully Logged out!")
    return redirect('home')