from django.db import models
from django.utils.translation import gettext_lazy as _
from entities.models import Entity


from django.db.models import Q, F, CheckConstraint


class Packaging(models.Model):
    id = models.AutoField(primary_key=True)
    length = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Length in cm"))
    width = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Width in cm"))
    height = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Height in cm"))
    volume = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Volume in litres"))
    net_weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Net weight in kg"))
    gross_weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Gross weight in kg"))
    name = models.CharField(max_length=255, default="Unnamed Packaging", verbose_name=_("Packaging name"), editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Packaging")
        verbose_name_plural = _("Packagings")
        constraints = [
            CheckConstraint(
                check=Q(gross_weight__gt=F('net_weight')),
                name="gross_weight_gt_net_weight",
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = f"{self.length}x{self.width}x{self.height}"
        super().save(*args, **kwargs)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70, verbose_name=_("Product name"))
    vendor = models.ForeignKey('entities.Entity', on_delete=models.CASCADE, related_name='vendor_products', verbose_name=_("Vendor"))
    description = models.TextField(verbose_name=_("Product description"))
    description_html = models.CharField(max_length=255, verbose_name=_("Product description HTML file"), default="",)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
    def __str__(self):
        return self.name



from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.utils.translation import gettext_lazy as _

class Stock(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='stock_entries', verbose_name=_("Product"))
    packaging = models.ForeignKey('Packaging', on_delete=models.CASCADE, related_name='stock_entries', verbose_name=_("Packaging"))
    quantity = models.IntegerField(verbose_name=_("Quantity of products in this packaging"))
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Price per packaging"))
    stock_quantity = models.IntegerField(verbose_name=_("Stock quantity of this packaging"), default=0)
    reserved_quantity = models.IntegerField(verbose_name=_("Reserved quantity"), default=0)
    ordered_quantity = models.IntegerField(verbose_name=_("Ordered quantity"), default=0)

    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")
        constraints = [
            CheckConstraint(
                check=Q(stock_quantity__gte=0),
                name="stock_quantity_non_negative",
            ),
            CheckConstraint(
                check=Q(reserved_quantity__gte=0),
                name="reserved_quantity_non_negative",
            ),
            CheckConstraint(
                check=Q(ordered_quantity__gte=0),
                name="ordered_quantity_non_negative",
            ),
            CheckConstraint(
                check=Q(reserved_quantity__lte=F('stock_quantity')),
                name="reserved_not_exceed_stock",
            ),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.packaging.name} (Price: {self.price}, In stock: {self.stock_quantity}, Reserved: {self.reserved_quantity}, Ordered: {self.ordered_quantity})"
