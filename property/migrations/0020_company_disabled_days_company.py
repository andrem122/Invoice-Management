# Generated by Django 2.1.15 on 2020-07-26 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0019_company_disabled_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_disabled_days',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.Company'),
        ),
    ]