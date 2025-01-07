from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Entity, Address, ContactPerson, BankAccount

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = (
        'display_name', 
        'company_name', 
        'entity_type', 
        'legal_entity_type', 
        'created_at', 
        'updated_at'
    )
    list_filter = ('entity_type', 'legal_entity_type')
    search_fields = ('display_name', 'company_name', 'company_id', 'company_vat')
    ordering = ('-created_at',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'entity', 
        'street', 
        'city', 
        'postal_code', 
        'country', 
        'address_type', 
        'created_at', 
        'updated_at'
    )
    list_filter = (
        'address_type', 
        'country')
    
    search_fields = (
        'street', 
        'city', 
        'Postal Code', 
        'Country'
    )
    ordering = ('-created_at',)

@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = (
        'entity', 
        'first_name', 
        'last_name', 
        'email', 
        'phone', 
        'position', 
        'is_primary', 
        'created_at', 
        'updated_at'
    )
    list_filter = ('is_primary',)
    search_fields = (
        'first_name', 
        'last_name', 
        'email', 
        'phone', 
        'position'
    )
    ordering = ('-created_at',)

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = (
        'entity', 
        'account_name', 
        'bank_account_number', 
        'iban', 
        'swift', 
        'bank_name', 
        'currency', 
        'is_primary', 
        'created_at', 
        'updated_at'
    )
    list_filter = (
        'is_primary', 
        'currency',
    )
    search_fields = (
        'account_name', 
        'bank_account_number', 
        'iban', 
        'swift', 
        'bank_name'
    )
    ordering = ('-created_at',)
