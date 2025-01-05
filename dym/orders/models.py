from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=70, verbose_name=_("Product name"))
    customer = models.ForeignKey('core.Entity', on_delete=models.CASCADE, verbose_name=_("Customer"))
    order_date = models.DateField(verbose_name=_("Order date"))
    required_date = models.DateField(verbose_name=_("Required delivery date"))
    shipped_date = models.DateField(verbose_name=_("Shipped date"))
    status = models.IntegerField(choices=[
        (0, _("New")),
        (1, _("Processing")),
        (2, _("Shipped")),
        (3, _("Delivered")),
        (4, _("Canceled")),
        (5, _("Awaiting Payment")),
        (6, _("Returned")),
        (7, _("Order Problem"))
    ], verbose_name=_("Status"))
    description_HTML = models.CharField(max_length=255, verbose_name=_("Comment in HTML format"))
    created_at = models.DateTimeField(default='CURRENT_TIMESTAMP', verbose_name=_("Created at"))
    updated_at = models.DateTimeField(default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP', verbose_name=_("Updated at"))

class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name=_("Order"))
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name=_("Product"))
    qty = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Quantity"))
    price_each = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price each"))
    created_at = models.DateTimeField(verbose_name=_("Created at"))
    updated_at = models.DateTimeField(verbose_name=_("Updated at"))

class Invoice(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name=_("Order"))
    customer = models.ForeignKey('core.Entity', on_delete=models.CASCADE, verbose_name=_("Customer"))
    issue_date = models.DateField(verbose_name=_("Invoice issue date"))
    due_date = models.DateField(verbose_name=_("Invoice due date"))
    payment_date = models.DateField(verbose_name=_("Payment date"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total invoice amount"))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Tax amount"))
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Subtotal amount"))
    status = models.IntegerField(choices=[
        (0, _("Issued")),
        (1, _("Paid")),
        (2, _("Awaiting Payment")),
        (3, _("Canceled"))
    ], verbose_name=_("Status"))
    description_HTML = models.CharField(max_length=255, verbose_name=_("Comment about the invoice"))
    created_at = models.DateTimeField(default='CURRENT_TIMESTAMP', verbose_name=_("Created at"))
    updated_at = models.DateTimeField(default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP', verbose_name=_("Updated at"))