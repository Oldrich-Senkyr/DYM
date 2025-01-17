


from django.db import models
from django.utils.translation import gettext_lazy as _
from entities.models import Entity


from django.db.models import Q, F, CheckConstraint

class ProductPackaging(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_packagings', verbose_name=_("Product"))
    packaging = models.ForeignKey('Packaging', on_delete=models.CASCADE, related_name='product_packagings', verbose_name=_("Packaging"))
    quantity = models.IntegerField(verbose_name=_("Quantity of products in this packaging"))

    class Meta:
        verbose_name = _("Product Packaging")
        verbose_name_plural = _("Product Packagings")

    def __str__(self):
        return f"{self.product.name} - {self.packaging.name} ({self.quantity})"


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
    qty_in_stock = models.IntegerField(verbose_name=_("In stock"))
    qty_reserved = models.IntegerField(verbose_name=_("In stock reserved"))
    qty_ordered = models.IntegerField(verbose_name=_("Ordered"))
    buy_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Buy price"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        constraints = [
            CheckConstraint(
            check=Q(qty_reserved__lte=F('qty_in_stock')),
            name="reserved_not_exceed_stock",
            ),
        ]
    def __str__(self):
        return self.name

from django.core.exceptions import ValidationError
class Order(models.Model):
    STATUS_CHOICES = [
        (0, _("New")),
        (1, _("Processing")),
        (2, _("Shipped")),
        (3, _("Delivered")),
        (4, _("Canceled")),
        (5, _("Awaiting Payment")),
        (6, _("Returned")),
        (7, _("Order Problem")),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70, verbose_name=_("Product name"))
    customer = models.ForeignKey('entities.Entity', on_delete=models.CASCADE, related_name='customer_orders', verbose_name=_("Customer"))
    order_date = models.DateField(verbose_name=_("Order date"))
    required_date = models.DateField(verbose_name=_("Required delivery date"))
    shipped_date = models.DateField(
        verbose_name=_("Shipped date"),
        null=True,
        blank=True,
    )
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name=_("Status"))
    description_html = models.CharField(max_length=255, verbose_name=_("Comment in HTML format"))
    created_at = models.DateTimeField( auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField( auto_now=True, verbose_name=_("Updated at"))

    def clean(self):
        if self.shipped_date and self.shipped_date < self.order_date:
            raise ValidationError(_("Shipped date cannot be earlier than the order date."))
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return self.name

class Invoice(models.Model):
    STATUS_CHOICES = [
        (0, _("Issued")),
        (1, _("Paid")),
        (2, _("Awaiting Payment")),
        (3, _("Canceled")),
    ]

    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='invoices', verbose_name=_("Order"))
    customer = models.ForeignKey('entities.Entity', on_delete=models.CASCADE, related_name='invoices', verbose_name=_("Customer"))
    issue_date = models.DateField(verbose_name=_("Invoice issue date"))
    due_date = models.DateField(verbose_name=_("Invoice due date"))
    payment_date = models.DateField(
        verbose_name=_("Payment date"),
        null=True,
        blank=True,
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total invoice amount"))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Tax amount"))
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Subtotal amount"))
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name=_("Status"))
    description_html = models.CharField(max_length=255, verbose_name=_("Comment about the invoice"))
    created_at = models.DateTimeField( auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField( auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    def save(self, *args, **kwargs):
        self.subtotal = self.total_amount - self.tax_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.id} for {self.customer.name} - {self.get_status_display()}"




class OrderProduct(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_products', verbose_name=_("Order"))
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_products', verbose_name=_("Product"))
    qty = models.IntegerField(verbose_name=_("Quantity"))
    price_each = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price per unit"))
    created_at = models.DateTimeField( auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField( auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Order Product")
        verbose_name_plural = _("Order Products")

    def __str__(self):
        return f"{self.product.name} - {self.qty} pcs @ {self.price_each}"
