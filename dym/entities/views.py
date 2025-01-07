from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Entity
from .forms import EntityForm, AddressFormSet, ContactPersonFormSet, BankAccountFormSet

def entity_create(request):
    if request.method == "POST":
        entity_form = EntityForm(request.POST)
        address_formset = AddressFormSet(request.POST, instance=Entity())
        contact_person_formset = ContactPersonFormSet(request.POST, instance=Entity())
        bank_account_formset = BankAccountFormSet(request.POST, instance=Entity())
        
        if (
            entity_form.is_valid()
            and address_formset.is_valid()
            and contact_person_formset.is_valid()
            and bank_account_formset.is_valid()
        ):
            entity = entity_form.save()
            address_formset.instance = entity
            address_formset.save()
            contact_person_formset.instance = entity
            contact_person_formset.save()
            bank_account_formset.instance = entity
            bank_account_formset.save()
            return redirect("/")  # Change to your list view or success page
            #return redirect("entity_list")  # Change to your list view or success page

    else:
        entity_form = EntityForm()
        address_formset = AddressFormSet(instance=Entity())
        contact_person_formset = ContactPersonFormSet(instance=Entity())
        bank_account_formset = BankAccountFormSet(instance=Entity())

    context = {
        "entity_form": entity_form,
        "address_formset": address_formset,
        "contact_person_formset": contact_person_formset,
        "bank_account_formset": bank_account_formset,
    }
    #return render(request, "entity_form.html", context)
    return render(request, "entities/entity_create.html", context)
    
