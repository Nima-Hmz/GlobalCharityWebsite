from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("title", "full_name", "email" , 'is_read_by_admin' )
    list_filter = ("created", 'is_read_by_admin')
    search_fields = ("title", "message",)
    list_editable = ['is_read_by_admin',]

@admin.register(ContactUsInfo)
class ContactUsInfoAdmin(admin.ModelAdmin):
    list_display = ['email' , 'loc' , 'phone']


@admin.register(Aboutus)
class AboutusAdmin(admin.ModelAdmin):
    list_display = ['Detail']