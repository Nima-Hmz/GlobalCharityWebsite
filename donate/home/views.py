from django.shortcuts import render
from django.views import View


# INdex View
class IndexView(View):
    def get(self, request):
        return render(request, 'home/home.html')
    
    def post(self, request):
        return render(request, 'home/home.html')
    
