from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import DonateLog
from accounts.models import User
import requests
import json
from django.views import View
from django.contrib import messages

# Create your views here.


class DonateView(View):
    def get(self, request):
        return render(request, "donate_logs/donate.html")
    
    def post(self, request):
        try: 
            amount = int(request.POST.get("amount"))
            currency = request.POST.get("currency")
        except:
            amount = 0
            currency = None

        if amount < 1000:
            messages.error(request, "مبلغ وارد شده باید بالای هزار تومان باشد", 'danger')
            return redirect('donate:donate')
        
        return redirect('donate:order_pay', amount=amount, currency=currency)
    

#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'



ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = 'http://127.0.0.1:8000/donate/vertify/'

class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, amount, currency):

        # make sure that currency is valid :
        list_of_currencies = ['TOMAN', 'DOLLAR', 'EURO', 'POUND', 'IQD', 'LIRA']
        if currency not in list_of_currencies:
            messages.error(request, "دوباره تلاش کنید", 'danger')
            return redirect("donate:donate")

        request.session["amount"] = {
            'amount':amount,
            'currency':currency
        }
    
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": amount,
            "Description": description,
            "Phone": '09398452352',
            "CallbackURL": CallbackURL,
        }
  
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    url = f"{ZP_API_STARTPAY}{response['Authority']}"
                    return redirect(url)
                else:
                    messages.error(request, "مشکل در اتصال به درگاه پرداخت", 'danger')
                    return redirect("home:index")
                
            messages.error(request, "مشکل در اتصال به درگاه پرداخت", 'danger')
            return redirect("home:index")
        
        except requests.exceptions.Timeout:
            messages.error(request, "پایان مهلت زمان اتصال", 'danger')
            return redirect("home:index")
        except requests.exceptions.ConnectionError:
            messages.error(request, "مشکل در اتصال", 'danger')
            return redirect("home:index")
        

class OrderVertifyView(LoginRequiredMixin, View):
    def get(self, request):
        user1 = request.user
        user_session = request.session['amount']
        authority = request.GET['Authority']
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": user_session['amount'],
            "Authority":authority
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:

                # successful pay :
                # create logs and other things here:

                # get the currency from user session
                currency = user_session['currency']

                # creating log here 
                user1 = request.user.phone_number
                user = User.objects.get(phone_number=user1)
                donate_log = DonateLog.objects.create(user=user, amount= user_session['amount'], currency=currency)
                donate_log.save()

                # add to total_donate here
                user.total_donate += int(user_session['amount'])
                user.save()

                del request.session['amount']
                messages.success(request, "تراکنش موفق بود", 'success')
                return redirect("home:index")
            
            else:
                messages.error(request, "تراکنش ناموفق بود و یا توسط کاربر لغو شد", 'danger')
                del request.session['amount']
                return redirect("home:index")
        else:
            messages.error(request, "تراکنش ناموفق بود و یا توسط کاربر لغو شد", 'danger')
            del request.session['amount']
            return redirect("home:index")
 

