# Generated by Django 4.1.7 on 2023-04-11 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0012_scheduleitems_prerout_schedule_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scheduleitems',
            old_name='prerout_schedule_item',
            new_name='preroute_schedule_item',
        ),
    ]
