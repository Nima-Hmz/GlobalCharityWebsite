# views.py
from django.shortcuts import render
from django.views.generic import TemplateView, View
from accounts.models import User
from django.db.models import Sum


# Stock View
class StockView(View):
    def get(self, request, *args, **kwargs):
        # Get top users with aggregated donation amounts
        top_users = User.objects.annotate(total_donation=Sum('total_donate')) \
                                .order_by('-total_donation')[:10]  # Limit to top 10 (adjust as needed)

        labels = [user.full_name for user in top_users]
        data = [user.total_donation for user in top_users]

        context = {'labels': labels, 'data': data}
        return render(request, 'stock/stock.html', context)
