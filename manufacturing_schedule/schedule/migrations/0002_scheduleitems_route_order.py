# Generated by Django 4.1.7 on 2023-04-22 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleitems',
            name='route_order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
