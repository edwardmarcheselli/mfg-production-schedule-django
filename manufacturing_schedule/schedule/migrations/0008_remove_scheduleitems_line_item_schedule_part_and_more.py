# Generated by Django 4.1.7 on 2023-04-09 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bom', '0011_alter_bom_line_items_and_more'),
        ('schedule', '0007_remove_scheduleitems_part_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheduleitems',
            name='line_item_schedule_part',
        ),
        migrations.AddField(
            model_name='scheduleitems',
            name='schedule_part',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_parts', to='bom.parts'),
        ),
        migrations.AddField(
            model_name='scheduleitems',
            name='schedule_release',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_releases', to='schedule.release'),
        ),
    ]
