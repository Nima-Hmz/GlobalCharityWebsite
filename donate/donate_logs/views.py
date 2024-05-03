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
                amount = user_session['amount']

                # make API request to get the latest currency value
                api_url = 'http://api.navasan.tech/latest/'
                api_params = {'item': 'usd', 'api_key': 'freeBqXyEcWjvEoGrGw8FkkrHkT9jkPe'}
                response = requests.get(api_url, params=api_params)
                if response.status_code == 200:
                    data = response.json()
                    usd_sell_rate = data['usd']  # assume this is the key for the USD sell rate
                    toman_per_usd = 1 / usd_sell_rate  # calculate Toman per USD

                # convert currency amount to Toman
                if currency == 'DOLLAR':
                    toman_amount = amount * toman_per_usd
                elif currency == 'EURO':
                    # convert Euro to Toman
                    euro_api_url = 'http://api.navasan.tech/latest/'
                    api_params1 = {'item': 'eur', 'api_key': 'freeBqXyEcWjvEoGrGw8FkkrHkT9jkPe'}
                    euro_response = requests.get(euro_api_url, api_params1=api_params1)
                    if euro_response.status_code == 200:
                        euro_data = euro_response.json()
                        euro_to_toman_rate = euro_data['rates']['IRR']  # Get the exchange rate from Euro to IRR (Iranian Rial)
                        toman_amount = amount * euro_to_toman_rate / 10  # Convert Euro to IRR and then to Toman (assuming 1 Toman = 10 IRR)
                    else:
                        toman_amount = None
                elif currency == 'POUND':
                    # convert Pound to Toman
                    pound_api_url = 'http://api.navasan.tech/latest/'
                    api_params2 = {'item': 'gbp', 'api_key': 'freeBqXyEcWjvEoGrGw8FkkrHkT9jkPe'}
                    pound_response = requests.get(pound_api_url, api_params2=api_params2)
                    if pound_response.status_code == 200:
                        pound_data = pound_response.json()
                        pound_to_toman_rate = pound_data['rates']['IRR']  # Get the exchange rate from POUND to IRR (Iranian Rial)
                        toman_amount = amount * pound_to_toman_rate / 10  # Convert POUND to IRR and then to Toman (assuming 1 Toman = 10 IRR)
                    else:
                        toman_amount = None
                elif currency == 'IQD':
                    # convert IQD to Toman
                    iqd_api_url = 'http://api.navasan.tech/latest/'
                    api_params3 = {'item': 'iqd', 'api_key': 'freeBqXyEcWjvEoGrGw8FkkrHkT9jkPe'}
                    iqd_response = requests.get(iqd_api_url, api_params3=api_params3)
                    if iqd_response.status_code == 200:
                        iqd_data = iqd_response.json()
                        iqd_to_toman_rate = iqd_data['rates']['IRR']  # Get the exchange rate from IQD to IRR (Iranian Rial)
                        toman_amount = amount * iqd_to_toman_rate / 10  # Convert IQD to IRR and then to Toman (assuming 1 Toman = 10 IRR)
                    else:
                        toman_amount = None
                elif currency == 'LIRA':
                    # convert LIRA to Toman
                    lira_api_url = 'http://api.navasan.tech/latest/'
                    api_params4 = {'item': 'try', 'api_key': 'freeBqXyEcWjvEoGrGw8FkkrHkT9jkPe'}
                    lira_response = requests.get(lira_api_url, api_params4=api_params4)
                    if lira_response.status_code == 200:
                        lira_data = lira_response.json()
                        lira_to_toman_rate  = lira_data['rates']['IRR']  # Get the exchange rate from LIRA to IRR (Iranian Rial)
                        toman_amount = amount * lira_to_toman_rate / 10  # Convert LIRA to IRR and then to Toman (assuming 1 Toman = 10 IRR)
                    else:
                        toman_amount = None
                else:
                    # handle other currencies or unknown currencies
                    toman_amount = None

                # make API request to get the latest gold price
                gold_api_url = 'http://api.navasan.tech/latest/'  # example API URL
                api_params_gold = {'item': '18ayar', 'api_key': 'freeBqXyEcWjvEoGrGw8FkkrHkT9jkPe'}
                gold_response = requests.get(gold_api_url, api_params_gold=api_params_gold)
                if gold_response.status_code == 200:
                    gold_data = gold_response.json()
                    gold_price = gold_data['XAU']['price']  # assume this is the key for the gold price

                    # convert Toman amount to gold
                    gold_value = toman_amount / gold_price

                # creating log here 
                user1 = request.user.phone_number
                user = User.objects.get(phone_number=user1)
                donate_log = DonateLog.objects.create(user=user, amount=amount, currency=currency)
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
 

