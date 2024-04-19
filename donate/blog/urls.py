from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path("", BlogListView.as_view(), name='blog_index'),
    path("article/", BlogDetailView.as_view(), name='blog_detail'),
]