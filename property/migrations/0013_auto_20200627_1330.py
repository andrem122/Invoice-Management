# Generated by Django 2.1.15 on 2020-06-27 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0012_auto_20200617_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='auto_respond_text',
            field=models.TextField(max_length=600, null=True),
        ),
    ]
