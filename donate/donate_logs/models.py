from django.db import models
from accounts.models import User

# Create your models here.


class DonateLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donator")
    amount = models.PositiveBigIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.amount}'
    

    class Meta:
        ordering = ('-date',)
