# Generated by Django 4.1.7 on 2023-04-09 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_scheduleitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='release_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]