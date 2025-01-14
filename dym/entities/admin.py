from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Entity, Address, ContactPerson, BankAccount


from django import forms
from django.contrib import admin
from .models import Entity

class EntityAdminForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = '__all__'

    # Změna velikosti inputu pro company_name
    company_name = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 400px;'}), label=_("Company name (First name, Last name)"))  # Lazy překlad)
    company_id = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 100px;'}), label=_('Company ID'))  # Zkráceno na polovinu
    company_vat = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 100px;'}), label=_('VAT ID'))  # Zkráceno na polovinu
   

class EntityAdmin(admin.ModelAdmin):
    form = EntityAdminForm
    list_display = ('company_name', 'created_at', 'updated_at')
    list_filter = ('company_name', 'company_id')
    search_fields = ('company_name', 'company_id', 'company_vat')
    ordering = ('-created_at',)

admin.site.register(Entity, EntityAdmin)


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
        'created_at', 
        'updated_at'
    )
    list_filter = (
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
