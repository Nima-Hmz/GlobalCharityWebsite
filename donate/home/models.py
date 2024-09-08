from django.db import models
from ckeditor.fields import RichTextField


#Contact us
class ContactUs(models.Model):
    title = models.CharField(max_length=100, verbose_name='موضوع')
    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(max_length=50, unique=True, default="@email", verbose_name='آدرس ایمیل')
    message = models.TextField(verbose_name='پیام شما')
    created = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده")
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)


    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    
    def __str__(self) -> str:
        return self.title

class ContactUsInfo(models.Model):
    email = models.EmailField(blank=True , null=True , verbose_name='ایمیل ما')
    loc   = models.TextField(blank=True , null=True , verbose_name='موقعیت ما')
    phone = models.CharField(blank=True , null=True , max_length=11 , verbose_name='تماس با ما')

    class Meta:
        verbose_name = ' اطلاعات تماس با ما '
        verbose_name_plural = 'اطلاعات تماس با ما'



#About-us
class Aboutus(models.Model):
    Detail = RichTextField(verbose_name='جزییات')


    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'
