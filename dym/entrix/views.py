from django.shortcuts import render, redirect
from agent.models import Person
from entrix.forms import PersonForm

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
