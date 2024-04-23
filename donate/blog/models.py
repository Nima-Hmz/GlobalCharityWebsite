from django.db import models
from ckeditor.fields import RichTextField

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
        verbose_name = "وبلاگ"
        verbose_name_plural = "بلاگ ها"

    def __str__(self):
        return str(self.title)