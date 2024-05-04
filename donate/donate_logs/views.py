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
        list_of_currencies = ['IRR', 'DOLLAR', 'EURO', 'POUND', 'IQD', 'LIRA']
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
                amount = user_session['amount']

                if currency == 'DOLLAR':
                    # make API request to get the latest currency value
                    api_url = 'http://api.navasan.tech/latest/'
                    api_params = {'item': 'usd', 'api_key': 'freeo7UvASyFBUGDuvsiZhwi3Mue3PyT'}
                    response = requests.get(api_url, params=api_params)
                    if response.status_code == 200:
                        usd_data = response.json()
                        """ assume this is the key for the USD sell rate """
                        usd_to_toman_rate = usd_data['usd']['value']
                        # print(usd_to_toman_rate)
                        # toman_per_usd = 1 / float(usd_sell_rate)  # calculate Toman per USD
                        # print(toman_per_usd)
                        """ convert currency amount to Toman """
                        toman_amount = amount * float(usd_to_toman_rate) / 1000 
                        # print(toman_amount)
                    else:
                        toman_amount = None
                elif currency == 'EURO':
                    # convert Euro to Toman
                    euro_api_url = 'http://api.navasan.tech/latest/'
                    api_params1 = {'item': 'eur', 'api_key': 'freeo7UvASyFBUGDuvsiZhwi3Mue3PyT'}
                    euro_response = requests.get(euro_api_url, params=api_params1)
                    if euro_response.status_code == 200:
                        euro_data = euro_response.json()
                        """ Get the exchnage rate from Euro to Toman """
                        euro_to_toman_rate = euro_data['eur']['value']
                        """ Convert Euro to Toman (amount = amoun that user donate) """   
                        toman_amount = amount * float(euro_to_toman_rate) / 1000
                        # print(toman_amount)
                    else:
                        toman_amount = None
                elif currency == 'POUND':
                    # convert Pound to Toman
                    pound_api_url = 'http://api.navasan.tech/latest/'
                    api_params2 = {'item': 'gbp', 'api_key': 'freeo7UvASyFBUGDuvsiZhwi3Mue3PyT'}
                    pound_response = requests.get(pound_api_url, params=api_params2)
                    if pound_response.status_code == 200:
                        pound_data = pound_response.json()
                        # print(pound_data)
                        """ Get the exchnage rate from Pound to Toman """
                        pound_to_toman_rate = pound_data['gbp']['value']
                        """ Convert Pound to Toman (amount = amoun that user donate) """  
                        toman_amount = amount * float(pound_to_toman_rate) / 1000
                        # print(toman_amount)  
                    else:
                        toman_amount = None
                elif currency == 'IQD':
                    # convert IQD to Toman
                    iqd_api_url = 'http://api.navasan.tech/latest/'
                    api_params3 = {'item': 'iqd', 'api_key': 'freeo7UvASyFBUGDuvsiZhwi3Mue3PyT'}
                    iqd_response = requests.get(iqd_api_url, params=api_params3)
                    if iqd_response.status_code == 200:
                        iqd_data = iqd_response.json()
                        """ Get the exchnage rate from IQD to Toman """
                        iqd_to_toman_rate = iqd_data['iqd']['value']
                        """ Convert IQD to Toman (amount = amoun that user donate) """
                        toman_amount = amount * float(iqd_to_toman_rate) / 1000
                        # print(toman_amount)
                    else:
                        toman_amount = None
                elif currency == 'LIRA':
                    # convert LIRA to Toman
                    lira_api_url = 'http://api.navasan.tech/latest/'
                    api_params4 = {'item': 'try', 'api_key': 'freeo7UvASyFBUGDuvsiZhwi3Mue3PyT'}
                    lira_response = requests.get(lira_api_url, params=api_params4)
                    if lira_response.status_code == 200:
                        lira_data = lira_response.json()
                        """ Get the exchnage rate from Euro to Toman """
                        lira_to_toman_rate  = lira_data['try']['value']
                        """ Convert Euro to Toman (amount = amoun that user donate) """
                        toman_amount = amount * float(lira_to_toman_rate) / 1000
                        # print(toman_amount)
                    else:
                        toman_amount = None
                
                elif currency == 'IRR':
                    # make API request to get the latest IRR price
                    irr_api_url = 'https://v6.exchangerate-api.com/v6/ab4a053319e602a65782e75e/latest/IRR'  # example API URL
                    irr_response = requests.get(irr_api_url)
                    if irr_response.status_code == 200:
                        irr_data = irr_response.json()
                        """ assume this is the key for the IRR rate """
                        irr_rate = irr_data['conversion_rates']['IRR']
                        """ convert IRR to Toman """
                        toman_amount = (amount * float(irr_rate)) / 10
                        print(toman_amount)
                    else:
                        toman_amount = None
                else:
                    """ handle other currencies or unknown currencies """
                    toman_amount = None

                """ make API request to get the latest gold price """
                gold_api_url = 'http://api.navasan.tech/latest/'  # example API URL
                api_params_gold = {'item': '18ayar', 'api_key': 'freeo7UvASyFBUGDuvsiZhwi3Mue3PyT'}
                gold_response = requests.get(gold_api_url, params=api_params_gold)
                if gold_response.status_code == 200:
                    gold_data = gold_response.json()
                    # print(gold_data)
                    """ assume this is the key for the gold price """
                    gold_price = gold_data['18ayar']['value']

                    if toman_amount is not None:
                        gold_value = toman_amount / float(gold_price)
                    else:
                        print("toman_amount is None. Please provide a valid value.")
                        gold_value = 0

                # creating log here 
                user1 = request.user.phone_number
                user = User.objects.get(phone_number=user1)
                donate_log = DonateLog.objects.create(user=user, amount=amount, currency=currency, gold_value=gold_value)
                donate_log.save()

                # add to total_donate here
                user.total_donate += gold_value
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
 

