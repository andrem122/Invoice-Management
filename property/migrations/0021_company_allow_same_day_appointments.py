# Generated by Django 2.1.15 on 2020-07-27 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0020_company_disabled_days_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='allow_same_day_appointments',
            field=models.BooleanField(default=True),
        ),
    ]