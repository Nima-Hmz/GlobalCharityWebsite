from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


# Create your models here.
class NewsletterEmailsModel(models.Model):
    email = models.EmailField(verbose_name='ایمیل')

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name_plural = 'ایمیل های خبرنامه'

class NewsletterMessageModel(models.Model):
    subject = models.CharField(max_length=100 , verbose_name='موضوع')
    message = models.TextField(verbose_name='متن خبر')

    def __str__(self):
        return f'{self.subject} - {self.message[:10]}'

    class Meta:
        verbose_name_plural = 'خبر جدید'
    
    def save_model(self, request, obj, form, change):
        subject = obj.subject
        message = obj.message

        emails = NewsletterEmailsModel.objects.all()

        for email in emails :
            receivers = email.email
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [receivers,]
            send_mail(subject, message, email_from, recipient_list )

        messages.success(request , 'انجام شد' , 'success')

        super().save_model(request, obj, form, change)
