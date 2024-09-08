from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import User


class blogModel(models.Model):
    title   = models.CharField(max_length=400 , verbose_name='عنوان')
    image   =  models.ImageField(upload_to='images/blog/%Y/%m/%d', verbose_name="تصویر مقاله")
    body    =  RichTextField(verbose_name='متن')
    slug    = models.SlugField(max_length=400 , verbose_name='اسلاگ' , unique=True , allow_unicode=True )
    status  = models.BooleanField(default=True , verbose_name='وضعیت انتشار')
    created = models.DateTimeField(auto_now_add = True, verbose_name="ایجاد شده")
    updated = models.DateTimeField(auto_now=True, verbose_name="به‌روز شده")
    lovely  = models.BooleanField(default=False , verbose_name='محبوب')

    class Meta:
        ordering = ("-updated",)
        verbose_name = "وبلاگی"
        verbose_name_plural = "بلاگ ها"

    def __str__(self):
        return str(self.title)
    

class commentModel(models.Model):
    blog = models.ForeignKey(blogModel , on_delete=models.CASCADE , related_name='blog_comment', verbose_name='برای وبلاگ')
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='user_comment', verbose_name='کاربر')

    name = models.CharField(max_length=40, verbose_name='نام')
    body = models.TextField(verbose_name='متن')

    date = models.DateTimeField(auto_now=True, verbose_name='منتشر شده')
    isActive    = models.BooleanField(default=True, verbose_name='نمایش داده شود؟')

    def __str__(self) -> str:
        return str(self.body[:8])
    
    class Meta:
        verbose_name_plural = 'نظرات'
        verbose_name = 'نظری'


class ReplyComment(models.Model):
    comment   = models.ForeignKey(commentModel , on_delete=models.CASCADE , related_name='recomment' , verbose_name='برای نظر')
    replyText = models.TextField(verbose_name='متن جواب')
    dateTime    = models.DateTimeField(auto_now=True)
    isActive    = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.replyText[:10]} ...'
    
    class Meta:
        verbose_name_plural = 'پاسخ ها'
        verbose_name = 'پاسخی'