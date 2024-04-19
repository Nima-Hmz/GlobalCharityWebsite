from django.shortcuts import render
from django.views import View


# BlogList View
class BlogListView(View):
    def get(self, request):
        return render(request, 'blog/blog-single.html')
    
    def post(self, request):
        return render(request, 'blog/blog-single.html')
    

# BlogDetail Us View
class BlogDetailView(View):
    def get(self, request):
        return render(request, 'blog/blog-single2.html')
    
    def post(self, request):
        return render(request, 'blog/blog-single2.html')
    