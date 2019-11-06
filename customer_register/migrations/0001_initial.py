# Generated by Django 2.1.7 on 2019-11-03 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paying', models.BooleanField(default=False, editable=False)),
                ('wants_sms', models.BooleanField(default=False)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, unique=True)),
                ('customer_type', models.CharField(choices=[('House Flipper', 'House Flipper'), ('Property Manager', 'Property Manager')], default='House Flipper', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]