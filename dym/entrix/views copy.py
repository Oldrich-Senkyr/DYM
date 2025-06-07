
from django.shortcuts import get_object_or_404, redirect, render
from agent.models import Person
from entrix.forms import PersonForm
from django.contrib import messages
from django.http import HttpResponse
import csv
from rfid.models import RFIDCard
from datetime import datetime, timedelta
from collections import defaultdict
from ingest.models import IngestedData
from django.utils.translation import gettext as _




def persons_list(request):
    persons = Person.objects.all()

    unique_id = request.GET.get('unique_id')
    if unique_id:
        persons = persons.filter(unique_id__icontains=unique_id)

    return render(request, 'entrix/persons-list.html', {
        'persons': persons,
    })




def person_add(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entrix:persons_list')
    else:
        form = PersonForm()

    return render(request, 'entrix/person-add.html', {
        'form': form,
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

    writer.writerow(['unique_id', 'display_name', 'first_name', 'last_name', 'role', 'title_before', 'title_after','email','phone'])
    for p in Person.objects.all():
        writer.writerow([
            p.unique_id,
            p.display_name,
            p.first_name,
            p.last_name,
            p.role,
            p.title_before,
            p.title_after,
            p.email,
            p.phone,
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
                        'email': row['email'],
                        'phone': row['phone'],
                        
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


def validate_sequence(entry_types):
    if not entry_types:
        return False
    if entry_types[0] != "1" or entry_types[-1] != "2":
        return False
    i = 1
    while i < len(entry_types) - 1:
        if entry_types[i] == "3":
            i += 1
            if i >= len(entry_types) - 1 or entry_types[i] != "1":
                return False
            i += 1
        else:
            return False
    return True

def persons_presence(request):
    selected_date = request.GET.get('date')
    raw_persons = Person.objects.all()

    # 1. Zpracování všech záznamů z IngestedData
    events_by_day = defaultdict(list)
    records = IngestedData.objects.all().order_by('received_at')

    for record in records:
        raw_data = record.data
        if isinstance(raw_data, str):
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                continue
        else:
            data = raw_data

        required_keys = ['date', 'time', 'entry_type', 'card_number', 'reader_id']
        if not all(k in data for k in required_keys):
            continue

        try:
            date_str = data['date'].strip("' ")
            time_str = data['time'].strip("' ")
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            entry_type = data['entry_type'].strip().strip(",'")
            card_number = data['card_number'].strip("' ")

            key = (date_str, card_number)
            events_by_day[key].append((dt, entry_type))
        except Exception:
            continue

    def validate_sequence(entry_types):
        if not entry_types or entry_types[0] != "1" or entry_types[-1] != "2":
            return False
        i = 1
        while i < len(entry_types) - 1:
            if entry_types[i] == "3":
                i += 1
                if i >= len(entry_types) - 1 or entry_types[i] != "1":
                    return False
                i += 1
            else:
                return False
        return True

    # 2. Vygeneruj data pro kazdou osobu
    persons = []
    for person in raw_persons:
        card = person.rfid_cards.first()
        card_number = card.card_id if card else None

        arrival = departure = work_time = break_time = validation = None

        if card_number and selected_date:
            key = (selected_date, card_number)
            events = events_by_day.get(key, [])
            events.sort()

            event_types = []
            breaks = []
            current_break_start = None

            for dt, etype in events:
                event_types.append(etype)
                if etype == "1":
                    if not arrival:
                        arrival = dt
                    elif current_break_start:
                        breaks.append((current_break_start, dt))
                        current_break_start = None
                elif etype == "3":
                    current_break_start = dt
                elif etype == "2":
                    departure = dt

            work_time = (departure - arrival) if arrival and departure else timedelta()
            break_time = sum((end - start for start, end in breaks), timedelta())
            validation = _("OK") if validate_sequence(event_types) else _("Invalid")

        persons.append({
            'unique_id': person.unique_id,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'get_role_display': person.get_role_display(),
            'card_number': card_number or '-',
            'arrival': arrival.strftime('%H:%M') if arrival else '-',
            'departure': departure.strftime('%H:%M') if departure else '-',
            'work_time': str(work_time) if work_time else '-',
            'break_time': str(break_time) if break_time else '-',
            'validation': validation or '-',
        })

    return render(request, 'entrix/persons-presence.html', {
        'persons': persons,
    })
