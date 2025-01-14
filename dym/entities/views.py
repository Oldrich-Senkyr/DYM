from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Entity
from .forms import EntityForm, AddressFormSet, ContactPersonFormSet, BankAccountFormSet


from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Entity

class EntityListView(ListView):
    model = Entity
    template_name = 'entity_list.html'
    context_object_name = 'entities'


class EntityEditView(UpdateView):
    model = Entity
    fields = ['display_name', 'company_name', 'legal_entity_type', 'company_id']
    template_name = 'entities/entity_edit.html'
    success_url = reverse_lazy('entities:entity_list')


class EntityDeleteView(DeleteView):  # tohle vola konfirmaci 
    model = Entity
    template_name = 'entities/entity_confirm_delete.html'
    success_url = reverse_lazy('entities:entity_list')

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import Entity

class EntityDeleteView(DeleteView): # Tohle je upravena metoda get ktera maze primo nebot konfirmace je v java scriptu
    model = Entity
    success_url = reverse_lazy('entities:entity_list')

    def get(self, request, *args, **kwargs):
        # Přímo smaže objekt bez potvrzovací stránky
        return self.delete(request, *args, **kwargs)



def entity_create_view(request):
    if request.method == "POST":
        entity_form = EntityForm(request.POST)
    
        if entity_form.is_valid():
            entity = entity_form.save()  # Uloží se entity a máme instanci
        
            # Přiřaďte uloženou entitu formsetům
            address_formset = AddressFormSet(request.POST, instance=entity)
            contact_person_formset = ContactPersonFormSet(request.POST, instance=entity)
            bank_account_formset = BankAccountFormSet(request.POST, instance=entity)

            if (
                address_formset.is_valid()
                and contact_person_formset.is_valid()
                and bank_account_formset.is_valid()
            ):
                # Uložení formsetů
                address_formset.save()
                contact_person_formset.save()
                bank_account_formset.save()
                return redirect("entities:entity_list")  # Přesměrování na seznam entit
            else:
               # Debugovací výpisy pro formsety, pokud nejsou validní
                
                print("entity_create_view - Address Formset Errors:")
                for form_index, form_errors in enumerate(address_formset.errors):
                    print(f"Form {form_index + 1}: {form_errors}")

                print("Contact Person Formset Errors:")
                for form_index, form_errors in enumerate(contact_person_formset.errors):
                    print(f"Form {form_index + 1}: {form_errors}")

                print("Bank Account Formset Errors:")
                for form_index, form_errors in enumerate(bank_account_formset.errors):
                    print(f"Form {form_index + 1}: {form_errors}")

        else:
            # Pokud `entity_form` není validní, přidejte debugovací výpis pro něj
            print(entity_form.errors)
            # Přidání popisu, odkud že chyby pocházejí
            for field, errors in entity_form.errors.items():
                for error in errors:
                    print(f"Error in {field} field: {error} (from entity)")

            
        
        # Vytvořte nové prázdné formsety pro renderování šablony
        address_formset = AddressFormSet(request.POST or None)
        contact_person_formset = ContactPersonFormSet(request.POST or None)
        bank_account_formset = BankAccountFormSet(request.POST or None)
    else:
        # GET request (prázdné formuláře)
        entity_form = EntityForm()
        address_formset = AddressFormSet()
        contact_person_formset = ContactPersonFormSet()
        bank_account_formset = BankAccountFormSet()

    context = {
        "entity_form": entity_form,
        "address_formset": address_formset,
        "contact_person_formset": contact_person_formset,
        "bank_account_formset": bank_account_formset,
    }
    return render(request, "entities/entity_create.html", context)
