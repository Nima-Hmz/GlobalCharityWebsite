# Generated by Django 5.0.4 on 2024-04-25 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactus',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='contactusinfo',
            name='iframe',
        ),
    ]
