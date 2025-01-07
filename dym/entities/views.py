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
    template_name = 'entity_edit.html'
    success_url = reverse_lazy('entity_list')

class EntityDeleteView(DeleteView):
    model = Entity
    template_name = 'entity_confirm_delete.html'
    success_url = reverse_lazy('entity_list')




def entity_create_view(request):
    if request.method == "POST":
        entity_form = EntityForm(request.POST)
    
        # `Entity()` není nutné, použije se instance vytvořená níže
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
                return redirect("entity_list")  # Přesměrování na seznam entit
        else:
            # Pokud entity_form není validní
            address_formset = AddressFormSet(request.POST)
            contact_person_formset = ContactPersonFormSet(request.POST)
            bank_account_formset = BankAccountFormSet(request.POST)
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
