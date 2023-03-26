from django.db import models

# Create your models here.
class Parts(models.Model):
    internal_pn = models.CharField(max_length=30)
    manufacturing_pn = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    weight = models.DecimalField(max_digits=7, decimal_places=3, null=True)

    class Routing(models.Choices):
        LASER = 1
        WELD = 2
        PRESS = 3
        MACHINE = 4
        CUT = 5
        PAINT = 6

    routing1 = models.IntegerField(choices=Routing.choices)
    routing2 = models.IntegerField(choices=Routing.choices)
    routing3 = models.IntegerField(choices=Routing.choices)
    routing4 = models.IntegerField(choices=Routing.choices)
    color = models.CharField(max_length=30)
    is_assembly = models.BooleanField(default=False)

class LineItemPart(models.Model):
    line_item_part = models.ForeignKey(Parts, on_delete=models.CASCADE, related_name="parts")
    qty = models.IntegerField()
    assembly_address = models.ForeignKey(Parts,on_delete=models.CASCADE, related_name="assembly_part", null=True)
    is_complete = models.BooleanField(default=False)
    calc_cost = models.DecimalField(max_digits=9, decimal_places=3, null=True)

class BOM(models.Model):
    line_items = models.ManyToManyField(LineItemPart, related_name="line_item_parts")
    calc_cost = models.DecimalField(max_digits=9, decimal_places=3, null=True)
    calc_date = models.DateField()