from django.contrib import admin
from .models import Packaging, Product, Stock


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor',)
    search_fields = ('name', 'vendor__name')
    list_filter = ('vendor',)
    ordering = ('name',)

@admin.register(Stock)
class ProductPackagingAdmin(admin.ModelAdmin):
    list_display = ('product', 'packaging', 'quantity')
    search_fields = ('product__name', 'packaging__name')
    list_filter = ('product',)

@admin.register(Packaging)
class PackagingAdmin(admin.ModelAdmin):
    list_display = ('name', 'length', 'width', 'height', 'volume', 'net_weight', 'gross_weight', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

