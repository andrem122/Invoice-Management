# Generated by Django 2.1.15 on 2020-03-12 00:26

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('customer_register', '0004_auto_20200310_1953'),
        ('appointments', '0002_auto_20191107_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment_Base',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('time', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('time_zone', timezone_field.fields.TimeZoneField(default='US/Eastern', editable=False)),
                ('appointment_task_id', models.CharField(blank=True, editable=False, max_length=50)),
                ('confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='customer_user',
        ),
        migrations.CreateModel(
            name='Appointment_Real_Estate',
            fields=[
                ('appointment_base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appointments.Appointment_Base')),
                ('apply_task_id', models.CharField(blank=True, editable=False, max_length=50)),
                ('unit_type', models.CharField(choices=[('', 'Unit Type'), ('3 Bedrooms', '3 Bedrooms'), ('2 Bedrooms', '2 Bedrooms'), ('1 Bedroom', '1 Bedroom')], default='', max_length=100)),
            ],
            bases=('appointments.appointment_base',),
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
        migrations.AddField(
            model_name='appointment_base',
            name='customer_user',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer_register.Customer_User'),
        ),
    ]