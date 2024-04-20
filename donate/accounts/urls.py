from django.urls import path 
from .views import *

app_name = 'account'

urlpatterns = [
    path("user_login/" , UserLoginView.as_view() , name='user_login'),
]
