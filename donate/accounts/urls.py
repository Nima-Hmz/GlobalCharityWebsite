from django.urls import path 
from .views import *

app_name = 'account'

urlpatterns = [
    path("user_login/" , UserLoginView.as_view() , name='user_login'),
    path("user_logout/", UserLogoutView.as_view(), name='user_logout'),
    path("user_register/", UserRegisterView.as_view(), name='user_register'),
    path("user_register_vertify/", UserRegisterVertifyView.as_view(), name='register_vertify'),
    path("user_forgotpassword/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("user_forgotpassword_vertify/", ForgotPasswordVertifyView.as_view(), name="forgot_password_vertify"),
    path("user_forgotpassword_newpass/", ForgotPasswordNewView.as_view(), name="new_password")
]
