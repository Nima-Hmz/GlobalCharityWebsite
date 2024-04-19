from django.shortcuts import render
from django.views import View


# Index View
class IndexView(View):
    def get(self, request):
        return render(request, 'home/index.html')
    
    def post(self, request):
        return render(request, 'home/index.html')
    



# About Us View
class AboutView(View):
    def get(self, request):
        return render(request, 'home/about.html')
    
    def post(self, request):
        return render(request, 'home/about.html')
    

# Contact Us View
class ContactView(View):
    def get(self, request):
        return render(request, 'home/contact.html')
    
    def post(self, request):
        return render(request, 'home/contact.html')