from django.urls import path , re_path
from .views import *

app_name = 'article'

urlpatterns = [
    path("", BlogListView.as_view(), name='blog_index'),
    re_path(r'article/(?P<slug>[-\w]+)/', BlogDetailView.as_view(), name='blog_detail'),
]