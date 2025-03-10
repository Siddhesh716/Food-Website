<<<<<<< HEAD
import json
from .models import Contact_us,Sign_up,Payment
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import random
import pandas as pd
import os
from django.contrib.auth import authenticate, logout as auth_logout
from datetime import datetime,time
from .decorators import log_errors
import requests
import numpy as np

# this views is downloading user entery and then deleting from db 
@log_errors
@csrf_protect
def delete_table1(request):

    signup_queryset = Sign_up.objects.using("project_user").all()
    contactus_queryset = Contact_us.objects.using("project_user").all()
    payment_queryset = Payment.objects.using("project_user").all()

    signup_df = pd.DataFrame(list(signup_queryset.values()))
    contactus_df = pd.DataFrame(list(contactus_queryset.values()))
    payment_df = pd.DataFrame(list(payment_queryset.values()))

    today_date = datetime.now().strftime('%d-%m-%Y')
    file_name = f'Data_{today_date}.xlsx'
    file_path = f'D:/project/harshada/TABLE DATA/{file_name}'
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        signup_df.to_excel(writer, sheet_name='Sign Up', index=False)
        contactus_df.to_excel(writer, sheet_name='Contact Us', index=False)
        payment_df.to_excel(writer, sheet_name='Payment', index=False)

    signup_queryset.delete()
    contactus_queryset.delete()
    payment_queryset.delete()

    template = loader.get_template("delete_table1.html")
    context = {"user": ""}
    return HttpResponse(template.render(context, request))

# base view in this some speicifc time website is closed and authentication is verified 
@log_errors
@csrf_protect
def login(request):
    user = request.user if request.user.is_authenticated else None
    now = datetime.now()
    restricted_start_time = time(9, 0)
    restricted_end_time = time(9, 5)
    if restricted_start_time <= now.time() <= restricted_end_time:
        return redirect('/delete_table1')
    else:
        return render(request,"Base.html", {'user': user})

# signup view taking inputs from user and storing in db
@log_errors
@csrf_protect
def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        mobile = request.POST.get("mobile")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if Sign_up.objects.using("project_user").filter(username=username).exists():
            template = loader.get_template("signup.html")
            context = {"user":""}
            messages.error(request, "Username Already Exists. Select Another Username.")
            return HttpResponse(template.render(context,request))
        elif (Sign_up.objects.using("project_user").create(first_name=first_name,last_name=last_name,mobile=mobile,username=username,password=password)):
            template = loader.get_template("Base.html")
            context = {"user":""}
            return HttpResponse(template.render(context,request))
    return render(request,'signup.html')

# verifying user credentials and giving access to website
@log_errors
@csrf_protect
def login_2(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if Sign_up.objects.using("project_user").filter(username=username,password=password).exists()== False:
            template = loader.get_template("login.html")
            context = {"user":""}
            messages.error(request, "INVALID USERNAME AND PASSWORD")
            return HttpResponse(template.render(context,request))
        if Sign_up.objects.using("project_user").filter(username=username).exists():
            user = Sign_up.objects.using("project_user").filter(username=username,password=password).values_list("username","password")
            x = list(user)
            if user is not None:
                if x[0][1] != password:
                    template = loader.get_template("login.html")
                    context = {"user":""}
                    messages.error(request, "INVALID USERNAME AND PASSWORD")
                    return HttpResponse(template.render(context,request))
                elif x[0][0] == username:
                    if x[0][1] == password:
                        template = loader.get_template("Base.html")
                        context = {"user":username}
                        return HttpResponse(template.render(context,request))
    return render(request,"login.html")

# menu page views
@log_errors
@csrf_protect
def Menu(request):
    return render(request,"Menu.html")

# list of selected food items views
@log_errors
@csrf_protect
def storage(request):
    return render(request,"storage.html")

# about us views
@log_errors
@csrf_protect
def About(request):
    return render(request,"About.html")

# services views
@log_errors
@csrf_protect
def Services(request):
    return render(request,"Services.html")

# contact us views
@log_errors
@csrf_protect
def Contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        Contact_us.objects.using("project_user").create(name=name,email=email,message=message)
        template = loader.get_template("Base.html")
        context = {"user":""}
        return HttpResponse(template.render(context,request))
    return render(request,"Contact.html")

# payment views storing user payment details in db and sending otp to mobile no
@log_errors
@csrf_protect
def payment13(request):
    if request.method == "POST":
        card_name = request.POST.get("card_name")
        card_no = request.POST.get("card_no")
        date = request.POST.get("date")
        cvv = request.POST.get("cvv")
        username = request.POST.get("username")
        try:
            user = Sign_up.objects.using("project_user").get(username=username)
        except Sign_up.DoesNotExist:
            messages.error(request,"INVALID USERNAME")
            return render(request,"payment.html")
        Payment.objects.using("project_user").create(card_name=card_name,card_no=card_no,date=date,cvv=cvv)
        global otp,mobile
        mobile = user.mobile
        otp = otp_genrator()
        # otp = url()
        request.session['otp'] = otp
        request.session['username'] = username
        messages.success(request, f"OTP IS SEND TO YOUR MOBILE")
        template = loader.get_template("otp_verification.html")
        context = {"user":username}
        return HttpResponse(template.render(context,request))
    return render(request,"payment.html")

# otp verifcation and storing user data in db
@log_errors
@csrf_protect
def otp_verification(request):
    if request.method == "POST":
        card_name = request.POST.get("card_name")
        card_no = request.POST.get("card_no")
        date = request.POST.get("date")
        cvv = request.POST.get("cvv")
        Payment.objects.using("project_user").create(card_name=card_name, card_no=card_no, date=date, cvv=cvv)
        messages.success(request, "PAYMENT SUCCESSFULL !!!")
        return render(request, "payment_success.html")
    return render(request, "otp_verification.html")

reotp = {"status": "false"}
new_old_otp = ""
old_otp = ""

# genration of random otp in this views
@log_errors
def otp_genrator():
    otp = np.random.randint(100000,999999)
    print("OTP FOR ASSIGNED MOBILE NO :-", otp)
    return otp

# resending otp to the user
@csrf_protect
@log_errors
def resend_otp(request):
    reotp["status"] = "sucess"
    global new_otp
    new_otp = otp_genrator()
    # new_otp = url()
    messages.success(request, f"OTP IS SEND TO YOUR MOBILE")
    context = {"data": new_otp}
    return render(request, "otp_verification.html", context)

# checking otp is expired or not in this views
@csrf_protect
@log_errors
def otp_expire(request):
    global old_otp, new_old_otp
    old_otp = otp
    if reotp["status"] == "sucess":
        new_old_otp = new_otp
    messages.error(request, "OTP IS EXPIRED CLICK RESEND OTP")
    context = {"otp": otp}
    return render(request, "otp_verification.html", context)

# taking inputs from user and verifying otp 
@csrf_protect
@log_errors
def Dashboard(request):
    if reotp["status"] == "sucess":
        if request.method == "POST":
            f1 = request.POST.get("f1")
            f2 = request.POST.get("f2")
            f3 = request.POST.get("f3")
            f4 = request.POST.get("f4")
            f5 = request.POST.get("f5")
            f6 = request.POST.get("f6")
            entered_otp = f1 + f2 + f3 + f4 + f5 + f6
            print("OTP ASSIGNED TO GIVEN MOBILE NO. :", new_otp)
            print("ENTERED OTP :-", entered_otp)
            if new_otp == new_old_otp:
                template = loader.get_template("otp_verification.html")
                context = {"page": "page"}
                messages.error(request, "OTP IS EXPIRED CLICK RESEND OTP")
                print("OTP IS Expired")
                return HttpResponse(template.render(context, request))
            elif str(new_otp) != entered_otp:
                template = loader.get_template("otp_verification.html")
                context = {"page": "page"}
                messages.error(request, "INCORRECT OTP ENTER CORRECT OTP")
                print("OTP IS INCORRECT")
                return HttpResponse(template.render(context, request))
            elif str(new_otp) == entered_otp:
                reotp["status"] = "false"
                print("THANK YOU !!!")
                return render(request, "paysuccess.html")
        else:
            template = loader.get_template("storage.html")
            context = {"user":""}
            return HttpResponse(template.render(context,request))
    else:
        if request.method == "POST":
            f1 = request.POST.get("f1")
            f2 = request.POST.get("f2")
            f3 = request.POST.get("f3")
            f4 = request.POST.get("f4")
            f5 = request.POST.get("f5")
            f6 = request.POST.get("f6")
            entered_otp = f1 + f2 + f3 + f4 + f5 + f6
            print("OTP ASSIGNED TO GIVEN MOBILE NO. :", otp)
            print("ENTERED OTP :-", entered_otp)
            if otp == old_otp:
                template = loader.get_template("otp_verification.html")
                context = {"page": "page"}
                messages.error(request, "OTP IS EXPIRED CLICK RESEND OTP")
                print("OTP IS EXPIRED")
                return HttpResponse(template.render(context, request))
            elif otp != int(entered_otp):
                template = loader.get_template("otp_verification.html")
                context = {"page": "page"}
                messages.error(request, "INCORRECT OTP ENTER CORRECT OTP")
                print("OTP IS INCORRECT")
                return HttpResponse(template.render(context, request))
            elif otp == int(entered_otp):
                print("THANK YOU !!!")
                return render(request, "paysuccess.html")
        else:
            template = loader.get_template("storage.html")
            context = {"user":""}
            return HttpResponse(template.render(context,request))

@log_errors
def url(mobile_number):
    url = "https://api2.juvlon.com/v5/sendSMS"
    otp = random.randint(100000,999999)
    print("OTP FOR ASSIGNED MOBILE NO :-", otp)
    data = {"apiKey": "OTgwODkjIyMyMDIzLTExLTE4IDE3OjU2OjEx", "mobile":  f"{mobile_number}" ,
         "body": "Dear User ,{var} is the OTP for your Selected Product. OTP is valid for 3 minutes only. Do not share this OTP with Anyone. - TMC-CLUSTER", "entityID": "1401379490000067172", "templateID": "1407170436371539405", "headerID": "TMCURP", "campaignName": "TEST SMS", "var": [{"value": otp}]}
    data_json = json.dumps(data)
    r = requests.post(url, data=data_json)

    print(r)
    return otp

# successfull page after complete payment procedure
@log_errors
@csrf_protect
def paysuccess(request):
    return render(request,"paysuccess.html")

# logout view 
@log_errors
@csrf_protect
def logout(request):
    request.session.clear()
    auth_logout(request)
    request.session.flush()  
=======
import json
from .models import Contact_us,Sign_up,Payment
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import random
import pandas as pd
import os
from django.contrib.auth import authenticate, logout as auth_logout
from datetime import datetime,time
from .decorators import log_errors
import requests

@log_errors
@csrf_protect
def delete_table1(request):

    signup_queryset = Sign_up.objects.using("project_user").all()
    contactus_queryset = Contact_us.objects.using("project_user").all()
    payment_queryset = Payment.objects.using("project_user").all()

    signup_df = pd.DataFrame(list(signup_queryset.values()))
    contactus_df = pd.DataFrame(list(contactus_queryset.values()))
    payment_df = pd.DataFrame(list(payment_queryset.values()))

    today_date = datetime.now().strftime('%d-%m-%Y')
    file_name = f'Data_{today_date}.xlsx'
    file_path = f'D:/project/harshada/TABLE DATA/{file_name}'
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        signup_df.to_excel(writer, sheet_name='Sign Up', index=False)
        contactus_df.to_excel(writer, sheet_name='Contact Us', index=False)
        payment_df.to_excel(writer, sheet_name='Payment', index=False)

    signup_queryset.delete()
    contactus_queryset.delete()
    payment_queryset.delete()

    template = loader.get_template("delete_table1.html")
    context = {"user": ""}
    return HttpResponse(template.render(context, request))

@log_errors
@csrf_protect
def login(request):
    user = request.user if request.user.is_authenticated else None
    now = datetime.now()
    restricted_start_time = time(9, 0)
    restricted_end_time = time(9, 5)
    if restricted_start_time <= now.time() <= restricted_end_time:
        return redirect('/delete_table1')
    else:
        return render(request,"Base.html", {'user': user})

@log_errors
@csrf_protect
def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        mobile = request.POST.get("mobile")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if Sign_up.objects.using("project_user").filter(username=username).exists():
            template = loader.get_template("signup.html")
            context = {"user":""}
            messages.error(request, "Username Already Exists. Select Another Username.")
            return HttpResponse(template.render(context,request))
        elif (Sign_up.objects.using("project_user").create(first_name=first_name,last_name=last_name,mobile=mobile,username=username,password=password)):
            template = loader.get_template("Base.html")
            context = {"user":""}
            return HttpResponse(template.render(context,request))
    return render(request,'signup.html')

@log_errors
@csrf_protect
def login_2(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if Sign_up.objects.using("project_user").filter(username=username,password=password).exists()== False:
            template = loader.get_template("login.html")
            context = {"user":""}
            messages.error(request, "INVALID USERNAME AND PASSWORD")
            return HttpResponse(template.render(context,request))
        if Sign_up.objects.using("project_user").filter(username=username).exists():
            user = Sign_up.objects.using("project_user").filter(username=username,password=password).values_list("username","password")
            x = list(user)
            if user is not None:
                if x[0][1] != password:
                    template = loader.get_template("login.html")
                    context = {"user":""}
                    messages.error(request, "INVALID USERNAME AND PASSWORD")
                    return HttpResponse(template.render(context,request))
                elif x[0][0] == username:
                    if x[0][1] == password:
                        template = loader.get_template("Base.html")
                        context = {"user":username}
                        return HttpResponse(template.render(context,request))
    return render(request,"login.html")

@log_errors
@csrf_protect
def Menu(request):
    return render(request,"Menu.html")

@log_errors
@csrf_protect
def storage(request):
    return render(request,"storage.html")

@log_errors
@csrf_protect
def About(request):
    return render(request,"About.html")

@log_errors
@csrf_protect
def Services(request):
    return render(request,"Services.html")

@log_errors
@csrf_protect
def Contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        Contact_us.objects.using("project_user").create(name=name,email=email,message=message)
        template = loader.get_template("Base.html")
        context = {"user":""}
        return HttpResponse(template.render(context,request))
    return render(request,"Contact.html")

@log_errors
@csrf_protect
def payment13(request):
    if request.method == "POST":
        card_name = request.POST.get("card_name")
        card_no = request.POST.get("card_no")
        date = request.POST.get("date")
        cvv = request.POST.get("cvv")
        username = request.POST.get("username")
        try:
            user = Sign_up.objects.using("project_user").get(username=username)
        except Sign_up.DoesNotExist:
            messages.error(request,"INVALID USERNAME")
            return render(request,"payment.html")
        Payment.objects.using("project_user").create(card_name=card_name,card_no=card_no,date=date,cvv=cvv)
        global otp,mobile
        mobile = user.mobile
        otp = otp_genrator()
        # otp = url()
        request.session['otp'] = otp
        request.session['username'] = username
        messages.success(request, f"OTP IS SEND TO YOUR MOBILE")
        template = loader.get_template("otp_verification.html")
        context = {"user":username}
        return HttpResponse(template.render(context,request))
    return render(request,"payment.html")

@log_errors
@csrf_protect
def otp_verification(request):
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        stored_otp = request.session.get('otp')

        if otp_input != stored_otp:
            messages.error(request, "Invalid OTP.")
            return render(request, "otp_verification.html")

        card_name = request.POST.get("card_name")
        card_no = request.POST.get("card_no")
        date = request.POST.get("date")
        cvv = request.POST.get("cvv")

        Payment.objects.using("project_user").create(card_name=card_name, card_no=card_no, date=date, cvv=cvv)
        messages.success(request, "PAYMENT SUCCESSFULL !!!")
        return render(request, "payment_success.html")

    return render(request, "otp_verification.html")

reotp = {"status": "false"}
new_old_otp = ""
old_otp = ""

@log_errors
def otp_genrator():
    otp = random.randint(100000, 999999)
    print("OTP FOR ASSIGNED MOBILE NO :-", otp)
    return otp

@csrf_protect
@log_errors
def resend_otp(request):
    reotp["status"] = "sucess"
    global new_otp
    new_otp = otp_genrator()
    # new_otp = url()
    messages.success(request, f"OTP IS SEND TO YOUR MOBILE")
    context = {"data": new_otp}
    return render(request, "otp_verification.html", context)

@csrf_protect
@log_errors
def otp_expire(request):
    global old_otp, new_old_otp
    old_otp = otp
    if reotp["status"] == "sucess":
        new_old_otp = new_otp
    messages.error(request, "OTP IS EXPIRED CLICK RESEND OTP")
    context = {"otp": otp}
    return render(request, "otp_verification.html", context)

@csrf_protect
@log_errors
def Dashboard(request):
    if reotp["status"] == "sucess":
        if request.method == "POST":
            f1 = request.POST.get("f1")
            f2 = request.POST.get("f2")
            f3 = request.POST.get("f3")
            f4 = request.POST.get("f4")
            f5 = request.POST.get("f5")
            f6 = request.POST.get("f6")
            entered_otp = f1 + f2 + f3 + f4 + f5 + f6
            print("OTP ASSIGNED TO GIVEN MOBILE NO. :", new_otp)
            print("ENTERED OTP :-", entered_otp)
            if new_otp == new_old_otp:
                template = loader.get_template("otp_verification.html")
                context = {"page": "page"}
                messages.error(request, "OTP IS EXPIRED CLICK RESEND OTP")
                print("OTP IS Expired")
                return HttpResponse(template.render(context, request))
            elif str(new_otp) != entered_otp:
                template = loader.get_template("otp_verification.html")
                context = {"page": "page"}
                messages.error(request, "INCORRECT OTP ENTER CORRECT OTP")
                print("OTP IS INCORRECT")
                return HttpResponse(template.render(context, request))
            elif str(new_otp) == entered_otp:
                reotp["status"] = "false"
                print("THANK YOU !!!")
                return render(request, "paysuccess.html")
        else:
            template = loader.get_template("storage.html")
            context = {"user":""}
            return HttpResponse(template.render(context,request))
    else:
        if request.method == "POST":
            f1 = request.POST.get("f1")
            f2 = request.POST.get("f2")
            f3 = request.POST.get("f3")
            f4 = request.POST.get("f4")
            f5 = request.POST.get("f5")
            f6 = request.POST.get("f6")
            entered_otp = f1 + f2 + f3 + f4 + f5 + f6
            print("OTP ASSIGNED TO GIVEN MOBILE NO. :", otp)
            print("ENTERED OTP :-", entered_otp)
            if otp == old_otp:
                template = loader.get_template("otp_verification.html")
                context = {"page": "page"}
                messages.error(request, "OTP IS EXPIRED CLICK RESEND OTP")
                print("OTP IS EXPIRED")
                return HttpResponse(template.render(context, request))
            elif otp != int(entered_otp):
                template = loader.get_template("otp_verification.html")
                context = {"page": "page"}
                messages.error(request, "INCORRECT OTP ENTER CORRECT OTP")
                print("OTP IS INCORRECT")
                return HttpResponse(template.render(context, request))
            elif otp == int(entered_otp):
                print("THANK YOU !!!")
                return render(request, "paysuccess.html")
        else:
            template = loader.get_template("storage.html")
            context = {"user":""}
            return HttpResponse(template.render(context,request))

@log_errors
def url(mobile_number):
    url = "https://api2.juvlon.com/v5/sendSMS"
    otp = random.randint(100000,999999)
    print("OTP FOR ASSIGNED MOBILE NO :-", otp)
    data = {"apiKey": "OTgwODkjIyMyMDIzLTExLTE4IDE3OjU2OjEx", "mobile":  f"{mobile_number}" ,
         "body": "Dear User ,{var} is the OTP for your Selected Product. OTP is valid for 3 minutes only. Do not share this OTP with Anyone. - TMC-CLUSTER", "entityID": "1401379490000067172", "templateID": "1407170436371539405", "headerID": "TMCURP", "campaignName": "TEST SMS", "var": [{"value": otp}]}
    data_json = json.dumps(data)
    r = requests.post(url, data=data_json)

    print(r)
    return otp

@log_errors
@csrf_protect
def paysuccess(request):
    return render(request,"paysuccess.html")

@log_errors
@csrf_protect
def logout(request):
    request.session.clear()
    auth_logout(request)
    request.session.flush()  
>>>>>>> 591af9b (Initial commit)
    return redirect('login')