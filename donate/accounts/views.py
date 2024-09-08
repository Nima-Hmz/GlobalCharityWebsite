from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from utils import send_otp_code
import random
from .models import User, OtpCodeModel
from django.contrib import messages
from django.utils import timezone
import datetime as my_datetime
from django.views import View

# User Login view.
class UserLoginView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "شما در حساب کاربری خود حضور دارید", 'danger')
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, 'accounts/login.html')
    
    def post(self , request):
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        user = authenticate(username=phone_number, password=password)
        if user is not None:
            login(request, user)
            messages.success(request , 'شما وارد حساب خود شدید' , 'success')
            return redirect("home:index")
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است", 'danger')
            return redirect("account:user_login")
        

class UserLogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request , 'شمار از حساب خود خارج شدید' , 'success')
        return redirect("home:index")
    
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request , 'شمار از حساب خود خارج شدید' , 'success')
        return redirect("home:index")


class UserRegisterView(View):
    def get(self , request):
        return render(request, 'accounts/register.html')
    
    def post(self, request):
        username_filed = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('conpass')
        display_name = request.POST.get('display_name')

        if password == confirm_password:
            if User.objects.filter(phone_number=phone_number).exists():
                messages.error(request, "شماره موبایل تکراری است", 'danger')
                return redirect("account:user_register")
            else:
                if len(phone_number) > 11 or len(phone_number) < 10:
                    messages.error(request, "شماره موبایل باید 11 رقم باشد", 'danger')
                    return redirect("account:user_register")
                else:
                    if OtpCodeModel.objects.filter(phone_number=phone_number).exists():
                        messages.error(request, "دوباره تلاش کنید", 'danger')
                        OtpCodeModel.objects.filter(phone_number=phone_number).delete()
                        return redirect("account:user_register")
                    else:
                        reandom_code = random.randint(1000, 9999)
                        print(f"-------\n{reandom_code}\n---------")
                        send_otp_code(phone_number=phone_number, code=reandom_code)
                        OtpCodeModel.objects.create(phone_number= phone_number, otp=reandom_code)
                        request.session["user_registration_info"] = {

                            'phone_number':phone_number,
                            'display_name':display_name,
                            'username':username_filed,
                            'password':password,

                        }
                        messages.success(request, "کد را برای شما از طریق پیامک ارسال کردیم", 'success')
                        return redirect("account:register_vertify")
                    

class UserRegisterVertifyView(View):

    def get(self, request):
        try:
            x = request.session['user_registration_info'] 
            return render(request, "accounts/register_vertify.html")

        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")
        
    def post(self, request):
        try:
            user_session = request.session['user_registration_info']
            code_instance = OtpCodeModel.objects.get(phone_number=user_session['phone_number'])
            user_input = int(request.POST.get("vertifycode"))
        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")


        if user_input == code_instance.otp:
            temp = code_instance.created
            temp += my_datetime.timedelta(seconds=120)
            now = timezone.now()
            if now < temp:

                # user = User.objects.create_user(username=user_session['username'], email=user_session['email'], password=user_session['password'])
                # user.save()
                # data = Customer(user=user, phone_number=user_session["phone_number"])
                # data.save()
                display_name1 = not bool(user_session['display_name'])

                user = User.objects.create_user(phone_number=user_session['phone_number'], full_name=user_session['username'], display_name=display_name1, password=user_session['password'])
                user.save()
                code_instance.delete()
                del request.session['user_registration_info']
                messages.success(request, "حساب کاربری شما ایجاد شد", 'success')

                #  login after register 
                our_user = authenticate(username=user_session['phone_number'], password=user_session['password'])
                if our_user is not None:
                    login(request, user)
                    return redirect("home:index")
              
            else:
                code_instance.delete()
                messages.error(request, "زمان شما به اتمام رسید", 'danger')
                return redirect('account:user_register')

        else:
            messages.error(request, "کد وارد شده اشتباه است", 'danger')
            return redirect('account:register_vertify')


class ForgotPasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.error(request, "شما در حساب خود حضور دارید", 'danger')
            return redirect("home:index")
        else:
            context = {
        
            }
            return render(request, "accounts/reset-password.html", context)
            
    def post(self, request):
        if request.user.is_authenticated:
            messages.error(request, "شما در حساب خود حضور دارید", 'danger')
            return redirect("home:index")
        else:
            phone_number = request.POST.get("phone_number")
            if phone_number != "":
                if User.objects.filter(phone_number=phone_number).exists():
                    if OtpCodeModel.objects.filter(phone_number=phone_number).exists():
                        messages.error(request, "دوباره تلاش کنید", 'danger')
                        OtpCodeModel.objects.filter(phone_number=phone_number).delete()
                        return redirect("account:forgot_password")

                    reandom_code = random.randint(1000, 9999)
                    send_otp_code(phone_number=phone_number, code=reandom_code)
                    OtpCodeModel.objects.create(phone_number= phone_number, otp=reandom_code)

                    request.session[0] = phone_number
                    request.session.save()

                    messages.success(request, "پیامک برای شما ارسال شد", 'success')
                    return redirect("account:forgot_password_vertify")
                else:
                    messages.error(request, "چنین کاربری وجود ندارد دوباره امتحان کنید", 'danger')
                    return redirect("account:forgot_password")
            else:
                messages.error(request, "فیلد درخواست شده را به درستی پر کنید", 'danger')
                return redirect("account:forgot_password")
            

class ForgotPasswordVertifyView(View):
    def get(self, request):
        try:
            x = request.session['0'] 
            context = {
        
            }
            return render(request, "accounts/register_vertify.html", context)
        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")
        
    def post(self, request):
        try:
            user_session = request.session["0"]
            code_instance = OtpCodeModel.objects.get(phone_number=user_session)
            user_input = int(request.POST.get("vertifycode"))
        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")

        if user_input == code_instance.otp:
            temp = code_instance.created
            temp += my_datetime.timedelta(seconds=120)
            now = timezone.now()
            if now < temp:
                code_instance.delete()
                messages.success(request, "شماره شما تایید شد. اکنون رمز جدید برای حساب خود ایجاد کنید", 'success')
                return redirect("account:new_password")
            else:
                code_instance.delete()
                messages.error(request, "زمان شما به اتمام رسید", 'danger')
                del request.session['0']
                return redirect("home:index")
        else:
            messages.error(request, "کد اشتباه است دوباره امتحان کنید", 'danger')
            return redirect("account:forgot_password_vertify")
            


class ForgotPasswordNewView(View):
    def get(self, request):
        try:
            x = request.session['0'] 
            context = {
        
            }
            return render(request, "accounts/reset-password2.html", context)
        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")
    
    def post(self, request):
        try:
            x = request.session['0']
        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")

        password = request.POST.get("password")
        if password != "":
            customer = User.objects.get(phone_number=request.session['0'])
            customer.set_password(password)
            customer.save()
            del request.session['0']
            messages.success(request, "رمز شما تغییر کرد اکنون میتوانید با رمز جدید وارد حساب خود شوید", 'success')
            return redirect("home:index")
        else:
            del request.session['0']
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect('home:index')
            
        
