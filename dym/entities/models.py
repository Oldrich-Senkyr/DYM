from django.db import models
from django.utils.translation import gettext_lazy as _

class Entity(models.Model):
    display_name = models.CharField(max_length=30, verbose_name=_("Display name"))
    company_name = models.CharField(max_length=70, verbose_name=_("Company name"))
    company_id = models.CharField(
    max_length=30, 
    unique=True, 
    null=False, 
    verbose_name=_("Company ID")
    )
    company_vat = models.CharField(max_length=20, verbose_name=_("Company VAT"))
    birth_number = models.CharField(max_length=10, verbose_name=_("Birth number"), blank=True, null=True)
    ENTITY_TYPE_CHOICES = [
        (1, _("Business")),
        (2, _("Non-profit")),
        (3, _("Contributory organization")),
    ]
    entity_type = models.IntegerField(choices=ENTITY_TYPE_CHOICES, verbose_name=_("Entity type"))
    LEGAL_ENTITY_TYPE_CHOICES = [
        (1, _("Legal entity")),
        (2, _("Natural person")),
     
    ]
    legal_entity_type = models.IntegerField(choices=LEGAL_ENTITY_TYPE_CHOICES, verbose_name=_("Legal entity type"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Entity")
        verbose_name_plural = _("Entities")

    def __str__(self):
        return self.company_name    

class Address(models.Model):
    entity = models.ForeignKey('Entity', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Entity"))
    street = models.CharField(max_length=100, verbose_name=_("Street"))
    city = models.CharField(max_length=50, verbose_name=_("City"))
    postal_code = models.CharField(max_length=20, verbose_name=_("Postal code"))
    country = models.CharField(max_length=50, verbose_name=_("Country"))
    address_type = models.IntegerField(choices=[
        (0, _("Billing")),
        (1, _("Shipping")),
        (2, _("Other"))
    ], verbose_name=_("Address type"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True,verbose_name=_("Updated at"))
    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"     

class ContactPerson(models.Model):
    entity = models.ForeignKey('Entity', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Entity"))
    first_name = models.CharField(max_length=50, verbose_name=_("First name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last name"))
    email = models.EmailField(verbose_name=_("Email address"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone number"))
    position = models.CharField(max_length=50, verbose_name=_("Position"))
    is_primary = models.BooleanField(default=False, verbose_name=_("Primary contact"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True,verbose_name=_("Updated at"))   
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"


class BankAccount(models.Model):
    entity = models.ForeignKey('Entity', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Entity"))
    account_name = models.CharField(max_length=50, verbose_name=_("Account name"))
    bank_account_number = models.CharField(max_length=30, verbose_name=_("Bank account number"))
    iban = models.CharField(max_length=34, verbose_name=_("IBAN"))
    swift = models.CharField(max_length=11, verbose_name=_("SWIFT code"))
    bank_name = models.CharField(max_length=100, verbose_name=_("Bank name"))
    currency = models.IntegerField(choices=[
        (0, _("CZK")),
        (1, _("EUR")),
        (2, _("USD")),
        (3, _("GBP")),
        (4, _("CHF")),        
    ], verbose_name=_("Account currency"))

    is_primary = models.BooleanField(default=False, verbose_name=_("Primary account"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    def __str__(self):
        return f"{self.bank_name} - {self.account_name} ({self.currency})"