from django.urls import path 
from .views import *

app_name = 'home'

urlpatterns = [
    path("" , IndexView.as_view() , name='index'),
    path("about/", AboutView.as_view(), name='about_us'),
    path("contact/", ContactUsView.as_view(), name='contact_us'),
    path("add-member/", NewslettersView.as_view(), name='add_member'),
]