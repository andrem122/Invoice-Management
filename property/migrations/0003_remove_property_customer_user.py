# Generated by Django 2.1.7 on 2019-11-07 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_auto_20191106_1614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='customer_user',
        ),
    ]
