# Generated by Django 4.1.1 on 2024-04-21 18:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donate_logs', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OtpCodeModel',
            new_name='DonateLog',
        ),
    ]