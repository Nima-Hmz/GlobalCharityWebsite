from django.contrib import admin
from .models import *

@admin.register(blogModel)
class blogAdmin(admin.ModelAdmin):
    list_display = ['title' , 'status'] 
    search_fields = ['title' , 'body']
    list_filter = ['status']
    prepopulated_fields = {'slug':('title',)}