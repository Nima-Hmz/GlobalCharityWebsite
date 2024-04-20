from django.urls import path 
from .views import *

app_name = 'account'

urlpatterns = [
    path("user_login/" , UserLoginView.as_view() , name='user_login'),
    path("user_logout/", UserLogoutView.as_view(), name='user_logout'),
    path("user_register/", UserRegisterView.as_view(), name='user_register'),
    path("user_register_vertify/", UserRegisterVertifyView.as_view(), name='register_vertify'),
]
