from django.contrib import admin
from .models import DonateLog

# Register your models here.



@admin.register(DonateLog)
class DonateLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'currency', 'amount' , 'date']
    search_fields = ['amount', 'currency']