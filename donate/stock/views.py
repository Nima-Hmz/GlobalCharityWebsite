from django.shortcuts import render
from django.views import View

# Stock View
class StockView(View):
    def get(self, request):
        return render(request, 'stock/stock.html')
    
    def post(self, request):
        return render(request, 'stock/stock.html')
