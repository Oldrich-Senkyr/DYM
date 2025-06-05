from django import forms
from .models import RFIDCard, CardPermission

class RFIDCardForm(forms.ModelForm):
    class Meta:
        model = RFIDCard
        fields = ['card_id', 'person', 'valid_from', 'valid_to']

class CardPermissionForm(forms.ModelForm):
    class Meta:
        model = CardPermission
        fields = ['card', 'permission']