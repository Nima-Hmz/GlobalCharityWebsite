from django.shortcuts import render , redirect
from django.views import View
from blog.models import blogModel
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from .models import *
from django.contrib import messages

# Index View
class IndexView(View):
    def get(self, request):
        blogs = blogModel.objects.filter(status=True).order_by('-updated')
        lovely_blogs = blogModel.objects.filter(status=True , lovely = True).order_by('-updated')[:3]

        paginator = Paginator(blogs , 2)
        page = request.GET.get('page',1)

        try :
            result = paginator.page(page)
        except PageNotAnInteger :
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)


        context = {
            'blogs' : result,
            'Lblogs' : lovely_blogs,
        }
        return render(request, 'home/index.html' , context=context)
    
    def post(self, request):
        return render(request, 'home/index.html')
    



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
        


