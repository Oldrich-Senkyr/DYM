from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import RFIDCard, Permission, CardPermission
from .forms import RFIDCardForm, CardPermissionForm

def card_list(request):
    cards = RFIDCard.objects.all()
    return render(request, 'rfid/card_list.html', {'cards': cards})

def card_create(request):
    if request.method == 'POST':
        form = RFIDCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rfid:card_list')
    else:
        form = RFIDCardForm()
    return render(request, 'rfid/card_form.html', {'form': form})

def card_permission_assign(request, card_id):
    card = get_object_or_404(RFIDCard, id=card_id)
    if request.method == 'POST':
        form = CardPermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rfid:card_list')
    else:
        form = CardPermissionForm(initial={'card': card})
    return render(request, 'rfid/assign_permission.html', {'form': form, 'card': card})
