# Generated by Django 2.1.15 on 2020-09-07 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_register', '0009_auto_20200907_1149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer_user_push_notification_tokens',
            old_name='push_notification_token',
            new_name='device_token',
        ),
    ]