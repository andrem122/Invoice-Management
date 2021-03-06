# Generated by Django 2.1.15 on 2020-04-07 17:42

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_auto_20200403_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='days_of_the_week_enabled',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('', 'Select All'), (0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')], default=None, max_length=14),
        ),
        migrations.AlterField(
            model_name='company',
            name='hours_of_the_day_enabled',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('', 'Select All'), (0, '12:00 AM'), (1, '1:00 AM'), (2, '2:00 AM'), (3, '3:00 AM'), (4, '4:00 AM'), (5, '5:00 AM'), (6, '6:00 AM'), (7, '7:00 AM'), (8, '8:00 AM'), (9, '9:00 AM'), (10, '10:00 AM'), (11, '11:00 AM'), (12, '12:00 PM'), (13, '1:00 PM'), (14, '2:00 PM'), (15, '3:00 PM'), (16, '4:00 PM'), (17, '5:00 PM'), (18, '6:00 PM'), (19, '7:00 PM'), (20, '8:00 PM'), (21, '9:00 PM'), (22, '10:00 PM'), (23, '11:00 PM')], default=None, max_length=62),
        ),
        migrations.AlterField(
            model_name='company',
            name='state',
            field=models.CharField(choices=[('', 'State'), ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default='', max_length=10),
        ),
    ]
