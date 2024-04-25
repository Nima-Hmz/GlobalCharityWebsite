from django.views.generic import TemplateView
from accounts.models import User
from django.db.models import Sum

class StockView(TemplateView):
    template_name = 'stock/stock.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve top 16 users with their total donations
        top_users = User.objects.annotate(total_donations=Sum('total_donate')).order_by('-total_donations')[:2]

        # Slice the top users into four groups of 4 users each
        # top_users1, top_users2, top_users3, top_users4 = [top_users[i:i+4] for i in range(0, 16, 4)]

        # Calculate total donations for each group of users
        total_donations = sum(user.total_donate for user in top_users)
        # total_donations1 = sum(user.total_donate for user in top_users1)
        # total_donations2 = sum(user.total_donate for user in top_users2)
        # total_donations3 = sum(user.total_donate for user in top_users3)
        # total_donations4 = sum(user.total_donate for user in top_users4)

        # Calculate final donation
        # final_donation = total_donations1 + total_donations2 + total_donations3 + total_donations4

        # Calculate percentage for each user
        for user in top_users:
            user.percent = (user.total_donate / total_donations) * 100 if total_donations!= 0 else 0

        # for user in top_users2:
        #     user.percent = (user.total_donate / total_donations) * 100 if total_donations!= 0 else 0

        # for user in top_users3:
        #     user.percent = (user.total_donate / total_donations) * 100 if total_donations!= 0 else 0

        # for user in top_users4:
        #     user.percent = (user.total_donate / total_donations) * 100 if total_donations!= 0 else 0

        context = {
            'top_users': top_users,
            # 'top_users1': top_users1,
            # 'top_users2': top_users2,
            # 'top_users3': top_users3,
            # 'top_users4': top_users4,
            # 'final_donation': final_donation,
        }
        return context