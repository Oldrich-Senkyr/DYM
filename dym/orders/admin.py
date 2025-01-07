from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from products.models import Product
from orders.models import Order, OrderProduct, Invoice
from core.models import Entity
from django.conf import settings

if settings.CURRENT_COMPANY == "dym":


    @admin.register(Order)
    class OrderAdmin(admin.ModelAdmin):
        list_display = (
            'name',
            'customer',
            'order_date',
            'required_date',
            'shipped_date',
            'status',
            'created_at',
            'updated_at',
        )
        list_filter = ('status', 'order_date', 'required_date', 'shipped_date')
        search_fields = ('name', 'customer__name')
        ordering = ('-created_at',)
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


    @admin.register(OrderProduct)
    class OrderProductAdmin(admin.ModelAdmin):
        list_display = (
            'order',
            'product',
            'qty',
            'price_each',
            'created_at',
            'updated_at',
        )
        search_fields = ('order__name', 'product__name')
        ordering = ('-created_at',)
        verbose_name = _("Order Product")
        verbose_name_plural = _("Order Products")


    @admin.register(Invoice)
    class InvoiceAdmin(admin.ModelAdmin):
        list_display = (
            'order',
            'customer',
            'issue_date',
            'due_date',
            'payment_date',
            'total_amount',
            'tax_amount',
            'subtotal',
            'status',
            'created_at',
            'updated_at',
        )
        list_filter = ('status', 'issue_date', 'due_date', 'payment_date')
        search_fields = ('order__name', 'customer__name')
        ordering = ('-created_at',)
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")





