from django.db import models

# Create your models here.
class ConstantVals(models.Model):
    steel_lb_price = models.DecimalField(max_digits=6, decimal_places=3)
    weld_hr_price = models.DecimalField(max_digits=5, decimal_places=2)
    laser_hr_price = models.DecimalField(max_digits=5, decimal_places=2)
    machine_hr_price = models.DecimalField(max_digits=5, decimal_places=2)
    cut_hr_price = models.DecimalField(max_digits=5, decimal_places=2)
    press_hr_price = models.DecimalField(max_digits=5, decimal_places=2)
    paint_hr_price = models.DecimalField(max_digits=5, decimal_places=2)

    laser_max_work = models.IntegerField(null=True)
    laser_worker_qty = models.IntegerField(null=True)

    weld_max_work = models.IntegerField(null=True)
    weld_worker_qty = models.IntegerField(null=True)

    press_max_work = models.IntegerField(null=True)
    press_worker_qty = models.IntegerField(null=True)

    machine_max_work = models.IntegerField(null=True)
    machine_worker_qty = models.IntegerField(null=True)

    cut_max_work = models.IntegerField(null=True)
    cut_worker_qty = models.IntegerField(null=True)

    paint_max_work = models.IntegerField(null=True)
    paint_worker_qty = models.IntegerField(null=True)
    
    post_date = models.DateField(null=True)

    class Meta:
        verbose_name = "Constant"