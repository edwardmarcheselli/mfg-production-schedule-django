# Generated by Django 4.1.7 on 2023-04-22 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConstantVals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('steel_lb_price', models.DecimalField(decimal_places=3, max_digits=6)),
                ('weld_hr_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('laser_hr_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('machine_hr_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cut_hr_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('press_hr_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('paint_hr_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('laser_max_work', models.IntegerField(null=True)),
                ('laser_worker_qty', models.IntegerField(null=True)),
                ('weld_max_work', models.IntegerField(null=True)),
                ('weld_worker_qty', models.IntegerField(null=True)),
                ('press_max_work', models.IntegerField(null=True)),
                ('press_worker_qty', models.IntegerField(null=True)),
                ('machine_max_work', models.IntegerField(null=True)),
                ('machine_worker_qty', models.IntegerField(null=True)),
                ('cut_max_work', models.IntegerField(null=True)),
                ('cut_worker_qty', models.IntegerField(null=True)),
                ('paint_max_work', models.IntegerField(null=True)),
                ('paint_worker_qty', models.IntegerField(null=True)),
                ('post_date', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'Constant',
            },
        ),
    ]
