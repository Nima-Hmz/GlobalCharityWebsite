# Generated by Django 5.0.4 on 2024-04-25 16:55

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_contactus_phone_remove_contactusinfo_iframe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aboutus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Detail', ckeditor.fields.RichTextField(verbose_name='جزییات')),
            ],
            options={
                'verbose_name': 'درباره ما',
                'verbose_name_plural': 'درباره ما',
            },
        ),
    ]
