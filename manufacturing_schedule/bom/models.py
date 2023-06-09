from django.db import models

# Create your models here.
class Parts(models.Model):
    internal_pn = models.CharField(max_length=30, null=True)
    manufacturing_pn = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=200, null=True)
    weight = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)

    class Routing(models.Choices):
        LASER = 1
        WELD = 2
        PRESS = 3
        MACHINE = 4
        CUT = 5
        PAINT = 6

    routing1 = models.IntegerField(choices=Routing.choices, null=True, blank=True)
    routing1_time = models.IntegerField(null=True, blank=True)
    routing2 = models.IntegerField(choices=Routing.choices, null=True, blank=True)
    routing2_time = models.IntegerField(null=True, blank=True)
    routing3 = models.IntegerField(choices=Routing.choices, null=True, blank=True)
    routing3_time = models.IntegerField(null=True, blank=True)
    routing4 = models.IntegerField(choices=Routing.choices, null=True, blank=True)
    routing4_time = models.IntegerField(null=True, blank=True)
    
    vendor1 = models.CharField(max_length=30, null=True)
    cost1 = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    is_active_vendor1 = models.BooleanField(default=False)

    vendor2 = models.CharField(max_length=30, null=True)
    cost2 = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    is_active_vendor2 = models.BooleanField(default=False)

    vendor3 = models.CharField(max_length=30, null=True)
    cost3 = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    is_active_vendor3 = models.BooleanField(default=False)

    is_assembly = models.BooleanField(default=False)
    is_purchased = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Company Part"

    def __str__(self):
        return self.internal_pn


class LineItemPart(models.Model):
    line_item_part = models.ForeignKey(Parts, on_delete=models.CASCADE, related_name="lineitem_parts")
    qty = models.IntegerField(null=True)
    assembly_address = models.ForeignKey('self',on_delete=models.CASCADE, related_name="lineitem_assembly_part", null=True)
    is_complete = models.BooleanField(default=False)
    calc_cost = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)

    class Meta:
        verbose_name = "BOM Line Item"
    
    def __str__(self):
        return 'ID:' + str(self.pk) + ' ' + ' | ' + str(self.line_item_part) + ' - ' + 'qty: ' + str(self.qty)

class BOM(models.Model):
    bom_name = models.CharField(max_length=30, null=True)
    line_items = models.ManyToManyField(LineItemPart, related_name="bom_line_item_parts")
    calc_cost = models.DecimalField(max_digits=9, decimal_places=3, null=True)

    class Meta:
        verbose_name = "BOM"

    def __str__(self):
        return self.bom_name