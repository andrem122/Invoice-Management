# Generated by Django 2.1.15 on 2020-07-16 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0014_auto_20200716_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='disabled_datetime_from',
        ),
        migrations.RemoveField(
            model_name='company',
            name='disabled_datetime_to',
        ),
    ]
