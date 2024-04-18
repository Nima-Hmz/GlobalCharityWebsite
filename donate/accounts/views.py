from django.shortcuts import render
from django.views import View

# User Login view.
class UserLoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        return render(request, 'accounts/login.html')
