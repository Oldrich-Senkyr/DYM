from django.db import models
from django.utils.translation import gettext_lazy as _


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class Order(models.Model):
    order_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Order number"),
        editable=False  # Číslo objednávky by nemělo být měnitelné ručně
    )
    customer = models.ForeignKey(
        'entities.Entity',
        on_delete=models.CASCADE,
        verbose_name=_("Customer")
    )
    order_date = models.DateField(default=now, verbose_name=_("Order date"))
    required_date = models.DateField(verbose_name=_("Required delivery date"))
    shipped_date = models.DateField(null=True, blank=True, verbose_name=_("Shipped date"))
    status = models.IntegerField(
        choices=[
            (0, _("New")),
            (1, _("Processing")),
            (2, _("Shipped")),
            (3, _("Delivered")),
            (4, _("Canceled")),
            (5, _("Awaiting Payment")),
            (6, _("Returned")),
            (7, _("Order Problem"))
        ],
        verbose_name=_("Status")
    )
    description_HTML = models.TextField(
        max_length=255,
        blank=True,
        verbose_name=_("Comment in HTML format")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created_at']  # Seřazení podle nejnovějších objednávek

    def __str__(self):
        return f"{self.order_number} - {self.customer}"

    def save(self, *args, **kwargs):
        # Automatické generování číslování objednávky
        if not self.order_number:
            year = now().year
            last_order = Order.objects.filter(order_date__year=year).order_by('id').last()
            if last_order:
                last_number = int(last_order.order_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            self.order_number = f"ORD-{year}{new_number:04d}"
        super().save(*args, **kwargs)


class OrderProduct(models.Model):
    order = models.ForeignKey(
        'Order', 
        on_delete=models.CASCADE, 
        related_name='order_products',  # Usnadňuje přístup k produktům v objednávce
        verbose_name=_("Order")
    )
    product = models.ForeignKey(
        'products.Product', 
        on_delete=models.CASCADE, 
        verbose_name=_("Ordered product")
    )
    qty = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_("Quantity")
    )
    price_each = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_("Price each")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Order Product")
        verbose_name_plural = _("Order Products")

    def __str__(self):
        return f"{self.qty} x {self.product} (Order #{self.order.id})"


class Invoice(models.Model):
    order = models.ForeignKey(
        'Order', 
        on_delete=models.CASCADE, 
        verbose_name=_("Order")
    )
    customer = models.ForeignKey(
        'entities.Entity', 
        on_delete=models.CASCADE, 
        verbose_name=_("Customer")
    )
    issue_date = models.DateField(verbose_name=_("Invoice issue date"))
    due_date = models.DateField(verbose_name=_("Invoice due date"))
    payment_date = models.DateField(null=True, blank=True, verbose_name=_("Payment date"))
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_("Total invoice amount")
    )
    tax_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_("Tax amount")
    )
    subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_("Subtotal amount")
    )
    status = models.IntegerField(
        choices=[
            (0, _("Issued")),
            (1, _("Paid")),
            (2, _("Awaiting Payment")),
            (3, _("Canceled"))
        ],
        verbose_name=_("Status")
    )
    description_HTML = models.TextField(
        max_length=255, 
        blank=True, 
        verbose_name=_("Comment about the invoice")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    def __str__(self):
        return f"Invoice for Order #{self.order.id}"


class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='sales', verbose_name=_("Sold product"))
    quantity = models.IntegerField(verbose_name=_("Quantity sold"))
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Sale price"))
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Sale date"))
    customer = models.ForeignKey('entities.Entity', on_delete=models.SET_NULL, null=True, blank=True, related_name='purchases', verbose_name=_("Customer"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Sale")
        verbose_name_plural = _("Sales")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} on {self.sale_date}"