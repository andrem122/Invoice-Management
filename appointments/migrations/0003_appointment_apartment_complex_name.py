# Generated by Django 2.1.7 on 2019-10-20 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_auto_20191009_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='apartment_complex_name',
            field=models.CharField(blank=True, editable=False, max_length=128),
        ),
    ]
