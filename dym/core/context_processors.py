from django.conf import settings

def current_company_flags(request):
    current_company = settings.CURRENT_COMPANY
    return {
        'CURRENT_COMPANY': current_company,
        'IS_DYM': current_company == "dym",
        'IS_VEROS': current_company == "veros",
    }
