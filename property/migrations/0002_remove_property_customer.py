# Generated by Django 2.1.7 on 2019-10-23 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='customer',
        ),
    ]
