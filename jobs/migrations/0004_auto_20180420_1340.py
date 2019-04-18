# Generated by Django 2.0.4 on 2018-04-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20180414_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='house',
            name='house_list_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
