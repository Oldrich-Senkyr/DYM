from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from entities.models import Entity
from products.models import Product, Packaging

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'vendor',
        'qty_in_stock',
        'qty_reserved',
        'qty_ordered',
        'buy_price',
        'created_at',
        'updated_at',
    )
    list_filter = ('vendor',)
    search_fields = ('name', 'vendor__name', 'description')
    ordering = ('-created_at',)
    verbose_name = _("Product")
    verbose_name_plural = _("Products")


@admin.register(Packaging)
class PackagingAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'length',
        'width',
        'height',
        'volume',
        'net_weight',
        'gross_weight',
        'created_at',
        'updated_at',
    )
    search_fields = ('product__name',)
    ordering = ('-created_at',)
    verbose_name = _("Packaging")
    verbose_name_plural = _("Packagings")


