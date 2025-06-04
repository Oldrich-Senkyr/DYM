
from django.shortcuts import get_object_or_404, redirect, render
from agent.models import Person
from entrix.forms import PersonForm
from django.contrib import messages

def persons_list(request):
    form = PersonForm()
    persons = Person.objects.all()

    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entrix:persons_list')

    unique_id = request.GET.get('unique_id')
    if unique_id:
        persons = persons.filter(unique_id__icontains=unique_id)

    return render(request, 'entrix/persons-list.html', {
        'form': form,
        'persons': persons,
    })


def edit_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, "Osoba byla úspěšně upravena.")
            return redirect('entrix:persons_list')
    else:
        form = PersonForm(instance=person)

    return render(request, 'entrix/person-form.html', {
        'form': form,
        'person': person,
        'is_editing': True,
    })


def delete_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    
    if request.method == 'POST':
        person.delete()
        messages.success(request, "Osoba byla smazána.")
        return redirect('entrix:persons_list')
    
    return render(request, 'entrix/person-delete.html', {
        'person': person
    })