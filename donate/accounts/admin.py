from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import *
from django.contrib.auth.models import Group



@admin.register(OtpCodeModel)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ['phone_number' , 'otp' , 'created']


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateinfoForm

    list_display = ['phone_number' , 'display_name', 'total_donate' , 'full_name' , 'is_admin']
    list_filter = ['is_admin']
    search_fields = ['phone_number' , 'full_name']

    fieldsets = (
            (None , {'fields' : ('phone_number' , 'display_name', 'total_donate' , 'full_name' , 'password')}),
            ('Permissions' , {'fields' : ('is_active' , 'is_admin', 'last_login')}),
    )

    add_fieldsets = (
        (None , {'fields':('phone_number' , 'display_name', 'total_donate' , 'full_name' , 'password1' , 'password2')}),
    )


    ordering = ['full_name']
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(User , UserAdmin)