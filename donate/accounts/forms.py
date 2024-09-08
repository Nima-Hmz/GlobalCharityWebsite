from typing import Any
from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

class UserCreateinfoForm(forms.ModelForm):
    password1 = forms.CharField(label='password' , widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password' , widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number' , 'full_name', 'display_name', 'total_donate')

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('password must match')

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        
        if commit:
            user.save()
        return user
        
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you cant change password using <a href=\"../password/\"> this form </a>")
    class Meta:
        model = User 
        fields = ('phone_number' , 'full_name' , 'password' , 'last_login', 'total_donate', 'display_name')

