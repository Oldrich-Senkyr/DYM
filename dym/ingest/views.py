from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from collections import OrderedDict
from .models import IngestedData
from django.conf import settings
import logging
from django.shortcuts import get_object_or_404, redirect

logger = logging.getLogger(__name__)

@csrf_exempt
def ingest_data(request):
    if request.method == 'POST':
        user_agent = request.headers.get('User-Agent', '').lower()
        is_browser = 'mozilla' in user_agent or 'chrome' in user_agent or 'safari' in user_agent
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        logger.info(f"User-Agent: {user_agent}")
        logger.info(f"Is browser: {is_browser}, Is AJAX: {is_ajax}")

        if not (is_browser or is_ajax):
            token = request.headers.get('Authorization', '')
            if not token.startswith('Bearer '):
                return JsonResponse({'error': 'Unauthorized: Missing or invalid Authorization token'}, status=401)
            if token.removeprefix("Bearer ") != settings.SECRET_INGEST_TOKEN:
                return JsonResponse({'error': 'Unauthorized: Invalid token'}, status=401)

        try:
            if is_browser or is_ajax:
                data = request.POST.get('data', '')
                if not data:
                    return JsonResponse({'error': 'No data provided in POST'}, status=400)
                payload = json.loads(data, object_pairs_hook=OrderedDict)
            else:
                payload = json.loads(request.body, object_pairs_hook=OrderedDict)

            ingested_data = IngestedData.objects.create(data=payload)
            response_data = OrderedDict([
                ("message", "Data ingested successfully!"),
                ("id", ingested_data.id)
            ])
            return JsonResponse(response_data, status=201)

        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An error occurred', 'details': str(e)}, status=500)

    # GET: Show ingested data, possibly filtered by card_number
    card_number = request.GET.get('card_number')
    ingested_data = IngestedData.objects.all().order_by('-received_at')

    if card_number:
        ingested_data = ingested_data.filter(data__card_number__icontains=card_number)

    return render(request, 'ingest/list.html', {
        'ingested_data': ingested_data
    })


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