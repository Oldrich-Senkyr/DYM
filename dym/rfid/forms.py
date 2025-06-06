from django import forms
from .models import RFIDCard, CardPermission
from django.utils.translation import gettext_lazy as _



class CardPermissionForm(forms.ModelForm):
    class Meta:
        model = CardPermission
        fields = ['permission']

    def __init__(self, *args, **kwargs):
        self.card = kwargs.pop('card', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        permission = cleaned_data.get('permission')
        if self.card and permission:
            if CardPermission.objects.filter(card=self.card, permission=permission).exists():
                raise forms.ValidationError(_("This permission is already assigned."))
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.card = self.card
        if commit:
            instance.save()
        return instance



class RFIDCardForm(forms.ModelForm):
    class Meta:
        model = RFIDCard
        fields = ['card_id', 'person', 'valid_from', 'valid_to']
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date'}),
            'valid_to': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'card_id': _("Card ID"),
            'person': _("Owner"),
            'valid_from': _("Valid From"),
            'valid_to': _("Valid To"),
        }
        help_texts = {
            'card_id': _("Enter the RFID card code."),
        }        