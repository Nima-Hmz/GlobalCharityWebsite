from django.shortcuts import render , redirect
from django.views import View
from blog.models import blogModel
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage

from .models import *
from django.contrib import messages

from django.views.generic import TemplateView
from accounts.models import User
from django.db.models import Sum
from donate_logs.models import DonateLog

from newsletters.models import *

from django.db.models import Q

# Index View
class IndexView(View):
    def get(self, request):
        blogs = blogModel.objects.filter(status=True).order_by('-updated')
        lovely_blogs = blogModel.objects.filter(status=True , lovely = True).order_by('-updated')[:3]

        # Get top users with aggregated donation amounts and gold values
        top_users = DonateLog.objects.values('user__full_name').annotate(total_donation=Sum('gold_value'), total_gold=Sum('gold_value')) \
                              .order_by('-total_donation')[:6]  # Limit to top 6 (adjust as needed)

        labels = [user['user__full_name'] for user in top_users]
        data_donation = [user['total_donation'] for user in top_users]
        limited_data_donation = []
        data_gold = [user['total_gold'] for user in top_users]
        limited_data_gold = []

        paginator = Paginator(blogs , 2)
        page = request.GET.get('page',1)

        try :
            result = paginator.page(page)
        except PageNotAnInteger :
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        


        for i in data_donation:
            j = "%.4f"%i
            limited_data_donation.append(j)

        
        for i in data_gold:
            j = "%.4f"%i
            limited_data_gold.append(j)


        query_name = request.GET.get("search")
        if query_name:
            result = blogModel.objects.filter(Q(title__icontains=query_name) | Q(body__icontains=query_name))

            
        context = {
            'blogs' : result,
            'Lblogs' : lovely_blogs,
            'top_users': top_users,
            'labels': labels,
            'data_donation': limited_data_donation, 
            'data_gold': limited_data_gold,
        }
        return render(request, 'home/index.html' , context=context)
    
    def post(self, request):

        context = {
            'users': User.objects.all()
        }

        return render(request, 'home/index.html', context)
    


# About Us View
class AboutView(View):
    def get(self, request):
        lovely_blogs = blogModel.objects.filter(status=True , lovely = True).order_by('-updated')[:3]

        details = Aboutus.objects.all()[:1]

        return render(request, 'home/about.html' , {'Lblogs' : lovely_blogs, 'details' : details})


# Contact Us
class ContactUsView(View):
    def get(self, request):
        contact_info = ContactUsInfo.objects.all()
        
        context = {
            'info' : contact_info,
            
        }
        return render(request, 'home/contact.html' , context=context)

    def post(self , request):
        name = request.POST['InputName']
        email = request.POST['InputEmail']
        subject = request.POST['InputSubject']
        message = request.POST['InputMessage']

        if name and email and subject and message:
            ticket = ContactUs(title=subject , full_name=name , email=email , message=message)
            ticket.save()
            ticket._meta.verbose_name_plural = "تماس با ما * "
            messages.success(request , 'پیام شما با موفقیت ارسال شد' , 'success')
            return redirect('home:contact_us')
        else:
            messages.error(request , 'پر کردن فیلد ها اجباری است' , 'danger')
            return redirect('home:contact_us')
        
class NewslettersView(View):
    def post(self , request):
        email = request.POST['email-field']

        member = NewsletterEmailsModel.objects.filter(email=email)

        if email:
            if member.exists():
                messages.error(request , 'این ایمیل قبلا ثبت شده است' , 'danger')
            else:
                new_member = NewsletterEmailsModel(email=email)
                new_member.save()

                messages.success(request , 'انجام شد' , 'success')

        return redirect('home:index')




class SearchResultsView(View):
    def get(self, request):

        
        
        query_name = request.GET.get("q")
        p_list = blogModel.objects.filter(Q(title__icontains=query_name) | Q(body__icontains=query_name))
        


        paginator = Paginator(p_list, 2)
        page = request.GET.get('page', 1)


        try :
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        
        url = request.get_full_path()
        context = {
            'p_list': result,
            'query_name': query_name,
            'categories': categories,
            'url': url,
            'best_seller': Product.objects.filter(best_seller=True),
            'offer': Product.objects.filter(offer=True),
            'star': Product.objects.filter(star=True),
            'brand':Product.objects.filter(brand=True),
        }

        return render(request, 'search/search_results.html', context)