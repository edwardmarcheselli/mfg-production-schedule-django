# Generated by Django 4.1.7 on 2023-04-09 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_projects_options'),
        ('schedule', '0002_alter_release_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='projects.projects'),
        ),
    ]
