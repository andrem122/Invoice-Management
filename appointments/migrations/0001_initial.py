# Generated by Django 2.1.7 on 2019-11-03 13:44

from django.db import migrations, models
import phonenumber_field.modelfields
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('time', models.DateTimeField()),
                ('appointment_task_id', models.CharField(blank=True, editable=False, max_length=50)),
                ('apply_task_id', models.CharField(blank=True, editable=False, max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('time_zone', timezone_field.fields.TimeZoneField(default='US/Eastern', editable=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('apartment_complex_name', models.CharField(blank=True, default=None, editable=False, max_length=128)),
                ('unit_type', models.CharField(choices=[('', 'Unit Type'), ('3 Bedrooms', '3 Bedrooms'), ('2 Bedrooms', '2 Bedrooms'), ('1 Bedroom', '1 Bedroom')], default='', max_length=100)),
            ],
        ),
    ]
