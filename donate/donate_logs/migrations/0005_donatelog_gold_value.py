# Generated by Django 5.0.4 on 2024-05-02 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donate_logs', '0004_alter_donatelog_options_donatelog_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='donatelog',
            name='gold_value',
            field=models.FloatField(default=0),
        ),
    ]
