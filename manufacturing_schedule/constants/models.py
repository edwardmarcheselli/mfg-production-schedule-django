from django.db import models

# Create your models here.
class ConstantVals(models.Model):
    steel_lb_price = models.DecimalField(..., max_digits=6, decimal_places=3)
    weld_hr_price = models.DecimalField(..., max_digits=5, decimal_places=2)
    laser_hr_price = models.DecimalField(..., max_digits=5, decimal_places=2)
    machine_hr_price = models.DecimalField(..., max_digits=5, decimal_places=2)
    cut_hr_price = models.DecimalField(..., max_digits=5, decimal_places=2)
    press_hr_price = models.DecimalField(..., max_digits=5, decimal_places=2)
    paint_hr_price = models.DecimalField(..., max_digits=5, decimal_places=2)
    post_date = models.DateField()