# Generated by Django 2.1.15 on 2020-07-22 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_register', '0006_remove_customer_user_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_user',
            name='wants_email_notifications',
            field=models.BooleanField(default=False),
        ),
    ]
