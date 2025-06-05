
from django.shortcuts import get_object_or_404, redirect, render
from agent.models import Person
from entrix.forms import PersonForm
from django.contrib import messages
from django.http import HttpResponse
import csv



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

def person_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    
    # Změna zde – nastavíme kódování UTF-8 s BOM
    response.write('\ufeff')  # UTF-8 BOM
    writer = csv.writer(response)

    writer.writerow(['unique_id', 'display_name', 'first_name', 'last_name', 'role', 'title_before', 'title_after'])
    for p in Person.objects.all():
        writer.writerow([
            p.unique_id,
            p.display_name,
            p.first_name,
            p.last_name,
            p.role,
            p.title_before,
            p.title_after
        ])

    return response



import csv
import codecs


def person_import_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
        reader = csv.DictReader(decoded_file)

        success_count = 0
        error_count = 0

        for row in reader:
            try:
                Person.objects.update_or_create(
                    unique_id=row['unique_id'],
                    defaults={
                        'display_name': row['display_name'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'role': row['role'],
                        'title_before': row['title_before'],
                        'title_after': row['title_after'],
                    }
                )
                success_count += 1
            except Exception as e:
                error_count += 1
                # Můžeš logovat chybu nebo ignorovat
                print(f"Chyba při zpracování řádku {row}: {e}")

        messages.success(request, f"Úspěšně importováno: {success_count}, chyb: {error_count}")
        return redirect('entrix:persons_list')

    return render(request, 'entrix/person_import.html')

