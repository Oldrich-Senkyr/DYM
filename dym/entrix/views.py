
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
import json




def persons_list(request):
    persons = Person.objects.all()

    unique_id = request.GET.get('unique_id')
    if unique_id:
        persons = persons.filter(unique_id__icontains=unique_id)

    # Rozšířený výstup o číslo karty
    enriched_persons = []
    for person in persons:
        card = person.rfid_cards.first()
        card_number = card.card_id if card else 'N/A'
        enriched_persons.append({
            'id': person.id,
            'unique_id': person.unique_id,
            'display_name': getattr(person, 'display_name', ''),
            'title_before': getattr(person, 'title_before', ''),
            'first_name': person.first_name,
            'last_name': person.last_name,
            'role': person.get_role_display(),
            'card_number': card_number
        })

    return render(request, 'entrix/persons-list.html', {
        'persons': enriched_persons,
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



def person_edit(request, pk):
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


def person_delete(request, pk):
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

#---------------------------------------------Presence  -------------------------------------------
from collections import defaultdict
from datetime import datetime, timedelta
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from ingest.models import CardEvent
from agent.models import Person


def clean_field(val):
    return str(val).strip().strip(",").strip("'").strip('"').upper()


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

def format_duration(td):
    total_minutes = int(td.total_seconds() // 60)
    rounded_minutes = total_minutes - (total_minutes % 5)
    hours = rounded_minutes // 60
    minutes = rounded_minutes % 60
    return f"{hours:02}:{minutes:02}"

def persons_presence(request):
    selected_date = request.GET.get('date')
    selected_date_obj = None
    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date_obj = None

    raw_persons = Person.objects.all()
    persons = []

    for person in raw_persons:
        cards = person.rfid_cards.all()
        selected_card = None
        presence = None

        for card in cards:
            card_number = clean_field(card.card_id)
            if selected_date_obj:
                events = CardEvent.objects.filter(
                    card_number=card_number,
                    date=selected_date_obj
                ).order_by('timestamp')

                if events.exists():
                    selected_card = card
                    break

        card_number = clean_field(selected_card.card_id) if selected_card else None

        if card_number and selected_date_obj:
            events = CardEvent.objects.filter(
                card_number=card_number,
                date=selected_date_obj
            ).order_by('timestamp')

            arrival = None
            departure = None
            breaks = []
            current_break_start = None
            event_types = []

            for event in events:
                dt = event.timestamp
                event_type = event.event_type
                event_types.append(event_type)

                if event_type == "1":
                    if not arrival:
                        arrival = dt
                    elif current_break_start:
                        breaks.append((current_break_start, dt))
                        current_break_start = None
                elif event_type == "3":
                    current_break_start = dt
                elif event_type == "2":
                    departure = dt

            work_time = (departure - arrival) if arrival and departure else timedelta()
            break_time = sum((end - start for start, end in breaks), timedelta())
            is_valid = validate_sequence(event_types)

            presence = {
                'arrival': arrival.strftime('%H:%M') if arrival else '-',
                'departure': departure.strftime('%H:%M') if departure else '-',
                'work_time': format_duration(work_time),
                'break_time': format_duration(break_time),
                'validation': "OK" if is_valid else "Invalid"
            }

        persons.append({
            'unique_id': person.unique_id,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'get_role_display': person.get_role_display(),
            'card_number': card_number if card_number else 'N/A',
            'arrival': presence['arrival'] if presence else '-',
            'departure': presence['departure'] if presence else '-',
            'work_time': presence['work_time'] if presence else '-',
            'break_time': presence['break_time'] if presence else '-',
            'validation': presence['validation'] if presence else 'Invalid',
        })

    return render(request, 'entrix/persons-presence.html', {
        'persons': persons,
        'selected_date': selected_date
    })


#---------------------------------------------Presence  -------------------------------------------
