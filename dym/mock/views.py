from collections import defaultdict
from datetime import datetime, timedelta
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from ingest.models import IngestedData
import json

def daily_summary(request):
    card_number_filter = request.GET.get('card')
    records = IngestedData.objects.all().order_by('received_at')
    events_by_day = defaultdict(list)

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

        card_number = data['card_number'].strip().strip("'")
        if card_number_filter and card_number != card_number_filter:
            continue

        try:
            date_str = data['date']
            time_str = data['time']
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            entry_type = data['entry_type'].strip().strip(",").strip("'")

            key = (data['date'], card_number)
            events_by_day[key].append((dt, entry_type))
        except Exception:
            continue

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

    summary = []
    for (date, card), events in events_by_day.items():
        events.sort()
        arrival = None
        departure = None
        breaks = []
        current_break_start = None
        event_types = []

        for dt, event_type in events:
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

        summary.append({
            'date': date,
            'card': card,
            'arrival': arrival.strftime('%H:%M') if arrival else '-',
            'departure': departure.strftime('%H:%M') if departure else '-',
            'work_time': str(work_time),
            'break_time': str(break_time),
            'validation': _("OK") if is_valid else _("BAD"),
        })

    return render(request, 'mock/daily-summary.html', {
        'summary': summary,
        'card_filter': card_number_filter,
    })
