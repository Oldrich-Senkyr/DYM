from django.db import models
from django.utils.translation import gettext_lazy as _
from .models import Entity

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=70, verbose_name=_("Product name"))
    vendor = models.ForeignKey('Entity', on_delete=models.CASCADE, verbose_name=_("Vendor"))
    description = models.TextField(verbose_name=_("Product description"))
    description_HTML = models.CharField(max_length=30, verbose_name=_("Product description HTML file"))
    qty_in_stock = models.IntegerField(verbose_name=_("In stock"))
    qty_reserved = models.IntegerField(verbose_name=_("In stock reserved"))
    qty_ordered = models.IntegerField(verbose_name=_("Ordered"))
    buy_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Buy price"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))


class Packaging(models.Model):
    length = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Length in cm"))
    width = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Width in cm"))
    height = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Height in cm"))
    volume = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Volume in litres"))
    net_weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Net weight in kg"))
    gross_weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Gross weight in kg"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name=_("Product"))