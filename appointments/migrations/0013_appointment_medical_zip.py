# Generated by Django 2.1.15 on 2020-07-31 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0012_appointment_medical_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment_medical',
            name='zip',
            field=models.CharField(default='', max_length=80),
        ),
    ]
