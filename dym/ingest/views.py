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
    if request.method == 'POST':
        # Rozpoznání, zda je požadavek z prohlížeče nebo API
        user_agent = request.headers.get('User-Agent', '').lower()
        is_browser = 'mozilla' in user_agent or 'chrome' in user_agent or 'safari' in user_agent
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        # Logování uživatelských agentů pro diagnostiku
        logger.info(f"User-Agent: {user_agent}")
        logger.info(f"Is browser: {is_browser}, Is AJAX: {is_ajax}")

        # Pokud není požadavek z prohlížeče, ověř token
        if not (is_browser or is_ajax):
            token = request.headers.get('Authorization', '')

            if token is None or not token.startswith('Bearer '):
                return JsonResponse({'error': 'Unauthorized: Missing or invalid Authorization token'}, status=401)

            # Ověření tokenu
            clean_token = token.removeprefix("Bearer ")
            if clean_token != settings.SECRET_INGEST_TOKEN:
                return JsonResponse({'error': 'Unauthorized: Invalid token'}, status=401)

        try:
            # Zpracování dat dle typu požadavku
            if is_browser or is_ajax:
                # Pokud je požadavek z prohlížeče, použij request.POST
                data = request.POST.get('data', '')
                if not data:
                    return JsonResponse({'error': 'No data provided in POST'}, status=400)
                payload = json.loads(data)
            else:
                # API požadavky s JSON
                payload = json.loads(request.body)

            # Uložení do databáze
            ingested_data = IngestedData.objects.create(data=payload)
            return JsonResponse({'message': 'Data ingested successfully!', 'id': ingested_data.id}, status=201)

        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            # Logování chyby pro diagnostiku
            logger.error(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An error occurred', 'details': str(e)}, status=500)

    # Zpracování GET požadavků (zobrazení seznamu)
    ingested_data = IngestedData.objects.all().order_by('-received_at')
    return render(request, 'ingest/list.html', {'ingested_data': ingested_data})


def export_data(request):
    # Načtení všech dat z databáze
    data = list(IngestedData.objects.values('id', 'data', 'received_at'))
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="ingested_data.json"'
    json.dump(data, response, indent=4, default=str)
    return response
