from django.shortcuts import render , get_object_or_404 , redirect
from django.views import View
from .models import *
from django.contrib import messages

# BlogList View
class BlogListView(View):
    def get(self, request):
        return render(request, 'blog/blog-single.html')
    
    def post(self, request):
        return render(request, 'blog/blog-single.html')
    

# BlogDetail Us View
class BlogDetailView(View):

    def setup(self, request, *args, **kwargs):
        self.blog = get_object_or_404(blogModel , slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request , slug):
        blog = self.blog
        comments = commentModel.objects.filter(blog__slug=slug , isActive=True)

        return render(request, 'blog/blog-single.html' , {'blog' : blog , 'comments' : comments})
    
    def post(self, request , slug):

        blog = self.blog
        name = request.POST['InputName']
        text = request.POST['InputComment']

        if name and text :
            new_comment = commentModel( user=request.user , blog=blog , name=name , body=text)
            new_comment.save()
            messages.success(request , 'نظر شما با موفقیت ثبت شد' , 'success')
        else:
            messages.error(request , 'فیلد ها اجباری است' , 'danger')
        
        return redirect('article:blog_detail' , slug)
    