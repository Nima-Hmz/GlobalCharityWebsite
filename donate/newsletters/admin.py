from django.contrib import admin
from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Register your models here.

admin.site.register(NewsletterEmailsModel)
@admin.register(NewsletterMessageModel)
class NewsLettersAdmin(admin.ModelAdmin):
     
     def save_model(self, request, obj, form, change):
        subject = obj.subject
        message = obj.message

        emails = NewsletterEmailsModel.objects.all()
        try:
            for email in emails :
                receivers = email.email
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [receivers,]
                send_mail(subject, message, email_from, recipient_list )

            messages.success(request , 'انجام شد' , 'success')

        except :
            messages.error(request , 'مشکل در انجام عملیات' , 'danger')

        super().save_model(request, obj, form, change)


