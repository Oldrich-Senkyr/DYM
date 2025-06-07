from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from collections import OrderedDict
from .models import IngestedData
from django.conf import settings
import logging
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
import csv
import io
from io import TextIOWrapper
from django.utils.timezone import now

logger = logging.getLogger(__name__)

@csrf_exempt
#ingest_data --------------------------------------------------------------------------------
@csrf_exempt
def ingest_data(request):
    if request.method == 'POST':
        if 'import_csv' in request.POST:
            csv_file = request.FILES.get('csv_file')
            if csv_file:
                try:
                    decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
                    reader = csv.DictReader(decoded_file)



                    
                    for row in reader:
                        # Zachovat původní názvy sloupců
                        record = {k: v.strip().strip("'") for k, v in row.items()}
                        IngestedData.objects.create(data=record, received_at=now())
                    messages.success(request, _("Data byla úspěšně importována."))
                except Exception as e:
                    messages.error(request, _("Chyba při importu CSV: ") + str(e))
            return redirect('ingest:read_data')

        else:
            # JSON import
            json_data = request.POST.get('data')
            try:
                parsed_data = json.loads(json_data)
                IngestedData.objects.create(data=json.dumps(parsed_data), received_at=now())
                messages.success(request, _("Data byla úspěšně uložena."))
            except json.JSONDecodeError:
                messages.error(request, _("Neplatný JSON."))
            return redirect('ingest:read_data')

    # GET request – výpis a filtrování
    card_number = request.GET.get('card_number')
    if card_number:
        ingested_data = IngestedData.objects.filter(data__icontains=card_number).order_by('-received_at')
    else:
        ingested_data = IngestedData.objects.all().order_by('-received_at')

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


