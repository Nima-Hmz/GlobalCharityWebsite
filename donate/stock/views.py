# views.py
from django.shortcuts import render
from django.views.generic import TemplateView, View
from donate_logs.models import DonateLog
from accounts.models import User
from django.db.models import Sum


# Stock View
class StockView(View):
    def get(self, request, *args, **kwargs):
        # Get top users with aggregated donation amounts and gold values
        top_users = DonateLog.objects.values('user__full_name').annotate(total_donation=Sum('gold_value'), total_gold=Sum('gold_value')) \
                              .order_by('-total_donation')[:10]  # Limit to top 10 (adjust as needed)

        labels = [user['user__full_name'] for user in top_users]
        data_donation = [user['total_donation'] for user in top_users]
        data_gold = [user['total_gold'] for user in top_users]

        context = {'labels': labels, 'data_donation': data_donation, 'data_gold': data_gold}
        return render(request, 'stock/stock.html', context)
