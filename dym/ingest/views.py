from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import IngestedData
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings



import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def ingest_data(request):
    # Logování všech hlaviček požadavku
    logger.debug(f"Request headers: {request.headers}")

    if request.method == 'POST':
        # Zkontrolujte, zda máte hlavičky
        user_agent = request.headers.get('User-Agent', '').lower()
        logger.debug(f"User-Agent: {user_agent}")

        is_browser = 'mozilla' in user_agent or 'chrome' in user_agent or 'safari' in user_agent
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        # Pokud není požadavek z prohlížeče, ověř token
        if not (is_browser or is_ajax):
            token = request.headers.get('Authorization', '')
            clean_token = token.removeprefix("Bearer ")
            if clean_token != settings.SECRET_INGEST_TOKEN:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

        try:
            # Pokud je požadavek z prohlížeče, použij request.POST
            if is_browser or is_ajax:
                payload = json.loads(request.POST.get('data', '{}'))
            else:  # API požadavky s JSON
                payload = json.loads(request.body)

            # Uložení do databáze
            ingested_data = IngestedData.objects.create(data=payload)
            return JsonResponse({'message': 'Data ingested successfully!', 'id': ingested_data.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred', 'details': str(e)}, status=500)

    # GET požadavky (zobrazení seznamu)
    ingested_data = IngestedData.objects.all().order_by('-received_at')
    return render(request, 'ingest/list.html', {'ingested_data': ingested_data})




def export_data(request):
    # Načtení všech dat z databáze
    data = list(IngestedData.objects.values('id', 'data', 'received_at'))
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="ingested_data.json"'
    json.dump(data, response, indent=4, default=str)
    return response

