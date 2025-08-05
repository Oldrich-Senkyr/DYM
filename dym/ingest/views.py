from django.utils.timezone import now
from ingest.models import IngestedData, CardEvent
from django.contrib import messages
from django.shortcuts import render, redirect
from io import TextIOWrapper
import csv
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
from collections import OrderedDict
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.http import HttpResponse
from pprint import pformat

logger = logging.getLogger(__name__)


#ingest_data --------------------------------------------------------------------------------
@csrf_exempt
def try_create_card_event(data):
    required = ['date', 'time', 'object_id', 'reader_id', 'entry_type', 'card_number']
    if not all(k in data for k in required):
        return

    try:
        dt_str = f"{data['date'].strip()} {data['time'].strip()}"
        timestamp = timezone.make_aware(datetime.strptime(dt_str, "%Y-%m-%d %H:%M"))
        CardEvent.objects.create(
            timestamp=timestamp,
            date=timestamp.date(),
            time=timestamp.time(),
            object_id=data['object_id'].strip(),
            reader_id=data['reader_id'].strip(),
            event_type=str(data['entry_type']).strip().strip("'").strip(','),
            card_number=data['card_number'].strip()
        )
    except Exception as e:
        logger.exception("Chyba při vytváření CardEventu")



@csrf_exempt
def ingest_data(request):
    logger.warning("Testovací warning zpráva z logu")

    if request.method == 'POST':
        logger.debug("Přijat POST request s tělem: %s", request.body)

        if 'import_csv' in request.POST:
            logger.debug("Detekován CSV import.")
            csv_file = request.FILES.get('csv_file')

            if csv_file:
                logger.info("Zpracovávám CSV soubor: %s", csv_file.name)
                try:
                    decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
                    reader = csv.DictReader(decoded_file)

                    for row in reader:
                        record = {k: v.strip().strip("'") for k, v in row.items()}
                        logger.debug("Importuji řádek: %s", record)

                        IngestedData.objects.create(data=record, received_at=now())
                        try_create_card_event(record)

                    messages.success(request, _("Data byla úspěšně importována."))
                    logger.info("CSV import proběhl úspěšně.")
                except Exception as e:
                    messages.error(request, _("Chyba při importu CSV: ") + str(e))
                    logger.exception("Výjimka při importu CSV souboru.")
            return redirect('ingest:read_data')

        else:
            logger.debug("Detekován JSON POST.")

            try:
                json_data = request.body.decode('utf-8')
                parsed_data = json.loads(json_data)
                logger.debug("Přijatý JSON: %s", parsed_data)

                IngestedData.objects.create(data=json.dumps(parsed_data), received_at=now())
                try_create_card_event(parsed_data)

                messages.success(request, _("Data byla úspěšně uložena."))
                logger.info("JSON data byla uložena.")

                # 🟩 Zde se vrací OK + celý request (hlavičky + tělo)
                response_text = f"OK\n\nHeaders:\n{pformat(dict(request.META))}\n\nBody:\n{json_data}"
                return HttpResponse(response_text, status=200, content_type="text/plain")

            except (json.JSONDecodeError, UnicodeDecodeError, AttributeError) as e:
                messages.error(request, _("Neplatný JSON."))
                logger.warning("Nepodařilo se dekódovat JSON: %s", e)
                return HttpResponse("Neplatný JSON", status=400, content_type="text/plain")

    card_number = request.GET.get('card_number')
    if card_number:
        logger.debug("Filtrovaný dotaz podle karty: %s", card_number)
        ingested_data = IngestedData.objects.filter(data__icontains=card_number).order_by('-received_at')
    else:
        ingested_data = IngestedData.objects.all().order_by('-received_at')
        logger.debug("Načítám všechny záznamy IngestedData.")

    return render(request, 'ingest/list.html', {'ingested_data': ingested_data})
#--------------------------------------------------------------------------------

def export_data(request):
    data = list(IngestedData.objects.values('id', 'data', 'received_at'))
    ordered_data = [OrderedDict([
        ("id", d["id"]),
        ("data", d["data"]),
        ("received_at", d["received_at"])
    ]) for d in data]

    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="ingested_data.json"'
    json.dump(ordered_data, response, indent=4, default=str)
    return response


@csrf_exempt
def delete_data(request, pk):
    if request.method == 'POST':
        obj = get_object_or_404(IngestedData, pk=pk)
        obj.delete()
        return redirect('ingest:read_data')
    return JsonResponse({'error': 'Invalid request method'}, status=405)


