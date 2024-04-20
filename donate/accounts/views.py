from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
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
