from django.shortcuts import render
from django.views import View

# Create your views here.


class DonateView(View):
    def get(self, request):
        return render(request, "donate_logs/donate.html")