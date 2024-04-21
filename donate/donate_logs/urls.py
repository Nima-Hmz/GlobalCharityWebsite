from django.urls import path 
from .views import *

app_name = 'donate'

urlpatterns = [
    path("", DonateView.as_view(), name="donate"),
    path("pay/<int:amount>/", OrderPayView.as_view(), name="order_pay"),
    path("vertify/", OrderVertifyView.as_view(), name="order_vertify"),
]