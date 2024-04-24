from django.views.generic import TemplateView
from accounts.models import User
from django.db.models import Sum

# Stock View
class StockView(TemplateView):
    template_name = 'stock/stock.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve top 16 users with their total donations
        top_users = User.objects.annotate(total_donations=Sum('total_donate')).order_by('-total_donations')[:16]
        
        # Calculate total donations
        total_donations = sum(user.total_donate for user in top_users)
        
        # Calculate percentage for each user
        for user in top_users:
            user.percent = (user.total_donate / total_donations) * 100 if total_donations != 0 else 0
        
        context['top_users'] = top_users
        return context