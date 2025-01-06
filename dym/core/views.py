from django.shortcuts import render, redirect

# Create your views here.

#Index page   --------------------------------------------------------------------------------------------------------
from django.shortcuts import render

def index(request):
    return render(request, 'core/base.html')

#Index page   ........................................................................................................
#Language switching  -------------------------------------------------------------------------------------------------
from django.utils import translation
from django.conf import settings
from urllib.parse import urlparse

def switch_language(request, language_code):
    # Aktivace nového jazyka
    translation.activate(language_code)

    # Uložení jazyka do cookies
    response = redirect('/')  # Výchozí přesměrování
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)

    # Zpracování refereru
    referer = request.META.get('HTTP_REFERER')
    if referer:
        parsed_referer = urlparse(referer)
        referer_path = parsed_referer.path

        # Detekce jazykového prefixu v URL
        for lang, _ in settings.LANGUAGES:
            if referer_path.startswith(f'/{lang}/'):
                # Nahrazení prefixu novým jazykem
                referer_path = referer_path.replace(f'/{lang}/', f'/{language_code}/', 1)
                break
        else:
            # Pokud prefix chybí, přidáme ho
            referer_path = f'/{language_code}{referer_path}'

        # Přesměrování na opravenou URL
        response = redirect(referer_path)

    return response
#Language switching  ......................................................................................
