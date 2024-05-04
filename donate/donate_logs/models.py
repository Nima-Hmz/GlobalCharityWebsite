from django.db import models
from accounts.models import User

# Create your models here.


class DonateLog(models.Model):
    CURRENCY_CHOICES = (
    ("IRR", "irr"),
    ("DOLLAR", "dollar"),
    ("EURO", "euro"),
    ("POUND", "pound"),
    ("IQD", "iqd"),
    ("LIRA", "lira"),
)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donator")
    amount = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=9,choices=CURRENCY_CHOICES, default="IRR")
    gold_value = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.amount}'
    

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = 'اطلاعات'
        verbose_name = 'اطلاعاتی'
