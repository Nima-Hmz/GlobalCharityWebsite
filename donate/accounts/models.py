from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11 , unique=True)
    full_name = models.CharField(max_length=124)
    display_name = models.BooleanField(default=True)
    total_donate = models.PositiveBigIntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name', 'display_name']

    def __str__(self) :
        return self.phone_number
    
    def has_perm(self , perm , obj=None):
        return True
    
    def has_module_perms(self , app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name_plural = 'کاربران'
        verbose_name = 'کاربری'
        

class OtpCodeModel(models.Model):
    phone_number = models.CharField(max_length=11)
    otp          = models.PositiveSmallIntegerField()
    created      = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.phone_number} - {self.otp} - {self.created}'
    
    class Meta:
        verbose_name_plural = 'کد های تایید'
        verbose_name = 'کد تاییدی'