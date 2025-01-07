from django import forms
from django.forms import inlineformset_factory
from .models import Entity, Address, ContactPerson, BankAccount

class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = '__all__'

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = '__all__'

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = '__all__'

AddressFormSet = inlineformset_factory(
    Entity, Address, form=AddressForm, extra=1, can_delete=True
)

ContactPersonFormSet = inlineformset_factory(
    Entity, ContactPerson, form=ContactPersonForm, extra=1, can_delete=True
)

BankAccountFormSet = inlineformset_factory(
    Entity, BankAccount, form=BankAccountForm, extra=1, can_delete=True
)
