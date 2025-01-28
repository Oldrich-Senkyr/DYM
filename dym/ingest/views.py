from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import IngestedData

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import IngestedData

@csrf_exempt
def ingest_data(request):
    if request.method == 'POST':
        try:
            # Zpracování formuláře
            if request.POST:
                payload = json.loads(request.POST.get('data', '{}'))
            else:
                # Zpracování POST JSON dat
                payload = json.loads(request.body)

            ingested_data = IngestedData.objects.create(data=payload)
            return JsonResponse({'message': 'Data ingested successfully!', 'id': ingested_data.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Zobrazení dat na stránce (GET požadavek)
    ingested_data = IngestedData.objects.all().order_by('-received_at')
    return render(request, 'ingest/index.html', {'ingested_data': ingested_data})


def export_data(request):
    # Načtení všech dat z databáze
    data = list(IngestedData.objects.values('id', 'data', 'received_at'))
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="ingested_data.json"'
    json.dump(data, response, indent=4, default=str)
    return response

