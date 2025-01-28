from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import IngestedData
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings







@csrf_exempt
def ingest_data(request):
    if request.method == 'POST':
        # Ověření tokenu
        token = request.headers.get('Authorization')
        clean_token = token.removeprefix("Bearer ")
        test_token = settings.SECRET_INGEST_TOKEN
        if clean_token != settings.SECRET_INGEST_TOKEN:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        try:
            # Zpracování dat na základě typu obsahu
            if request.content_type == 'application/json':
                payload = json.loads(request.body)
            else:
                payload = json.loads(request.POST.get('data', '{}'))

            # Vytvoření záznamu v databázi
            ingested_data = IngestedData.objects.create(data=payload)
            return JsonResponse({'message': 'Data ingested successfully!', 'id': ingested_data.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            # Logování chyby (volitelné)
            return JsonResponse({'error': 'An error occurred', 'details': str(e)}, status=500)

    # Zpracování GET požadavku
    ingested_data = IngestedData.objects.all().order_by('-received_at')
    return render(request, 'ingest/list.html', {'ingested_data': ingested_data})



def export_data(request):
    # Načtení všech dat z databáze
    data = list(IngestedData.objects.values('id', 'data', 'received_at'))
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="ingested_data.json"'
    json.dump(data, response, indent=4, default=str)
    return response

