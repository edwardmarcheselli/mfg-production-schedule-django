# Generated by Django 4.1.7 on 2023-04-22 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_routetask'),
    ]

    operations = [
        migrations.AddField(
            model_name='routetask',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'Active'), (2, 'Suspended'), (3, 'Compelte'), (4, 'Failed')], null=True),
        ),
    ]
