from django.urls import path 
from .views import *

app_name = 'home'

urlpatterns = [
    path("", DonateView.as_view(), name="donate")
]