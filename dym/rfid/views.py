from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import RFIDCard, Permission, CardPermission
from .forms import RFIDCardForm, CardPermissionForm
from django.contrib import messages
from django.utils.translation import gettext as _

def card_list(request):
    cards = RFIDCard.objects.all()
    return render(request, 'rfid/card-list.html', {'cards': cards})

def card_create(request):
    if request.method == 'POST':
        form = RFIDCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rfid:card-list')
    else:
        form = RFIDCardForm()
    return render(request, 'rfid/card-edit.html', {'form': form})

def card_permission_assign(request, card_id):
    card = get_object_or_404(RFIDCard, id=card_id)

    if request.method == 'POST':
        form = CardPermissionForm(request.POST, card=card)
        if form.is_valid():
            form.save()
            messages.success(request, _("Oprávnění bylo přiřazeno."))
            return redirect('rfid:card_permission_assign', card_id=card.id)
    else:
        form = CardPermissionForm(card=card)

    return render(request, 'rfid/assign-permission.html', {
        'form': form,
        'card': card,
    })

def card_update(request, pk):
    card = get_object_or_404(RFIDCard, pk=pk)
    if request.method == 'POST':
        form = RFIDCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, _("Card updated successfully."))
            return redirect('rfid:card_list')
    else:
        form = RFIDCardForm(instance=card)
    return render(request, 'rfid/card-edit.html', {'form': form, 'card': card})


def card_delete(request, pk):
    card = get_object_or_404(RFIDCard, pk=pk)
    if request.method == 'POST':
        card.delete()
        messages.success(request, _("Card deleted successfully."))
        return redirect('rfid:card_list')
    return render(request, 'rfid/card-confirm-delete.html', {'card': card})

def remove_permission(request, card_id, permission_id):
    card = get_object_or_404(RFIDCard, id=card_id)
    permission = get_object_or_404(Permission, id=permission_id)
    CardPermission.objects.filter(card=card, permission=permission).delete()
    messages.success(request, _("Oprávnění bylo odebráno."))
    return redirect("rfid:card_permission_assign", card_id=card_id)