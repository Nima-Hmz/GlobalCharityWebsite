# Generated by Django 5.0.4 on 2024-05-02 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletteremailsmodel',
            options={'verbose_name': 'ایمیلی', 'verbose_name_plural': 'ایمیل های خبرنامه'},
        ),
        migrations.AlterModelOptions(
            name='newslettermessagemodel',
            options={'verbose_name': 'خبری', 'verbose_name_plural': 'خبر جدید'},
        ),
        migrations.AlterField(
            model_name='newslettermessagemodel',
            name='message',
            field=models.TextField(verbose_name='متن خبر'),
        ),
    ]