from django import forms
from agent.models import Person



class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['unique_id', 'display_name', 'first_name', 'last_name', 'role', 'title_before', 'title_after','email','phone']
        widgets = {
            'unique_id': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'display_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'role': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'title_before': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'title_after': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'email': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
        
        }

        def clean_unique_id(self):
            unique_id = self.cleaned_data['unique_id']
            qs = Person.objects.filter(unique_id__iexact=unique_id)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Toto ID osoby již existuje.")
            return unique_id

        def clean_display_name(self):
            display_name = self.cleaned_data['display_name']
            qs = Person.objects.filter(display_name__iexact=display_name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Zobrazované jméno už existuje.")
            return display_name