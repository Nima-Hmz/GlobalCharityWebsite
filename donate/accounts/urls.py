from django.urls import path 
from .views import *

app_name = 'account'

urlpatterns = [
    path("" , UserLoginView.as_view() , name='user_login'),
]
