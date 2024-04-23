from django.shortcuts import render
from django.views import View
from blog.models import blogModel
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage


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
        return render(request, 'home/about.html')
    
    def post(self, request):
        return render(request, 'home/about.html')
    

# Contact Us View
class ContactView(View):
    def get(self, request):
        return render(request, 'home/contact.html')
    
    def post(self, request):
        return render(request, 'home/contact.html')