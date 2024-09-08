from django.urls import path 
from .views import *

app_name = 'stock'

urlpatterns = [
    path("" , StockView.as_view(), name='stock'),
]