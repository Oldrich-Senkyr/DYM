import logging

logger = logging.getLogger(__name__)

from django.conf import settings

class LogHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "LOG_HOST_MIDDLEWARE_ENABLED", False):
            logger.info(f"HTTP_HOST: {request.META.get('HTTP_HOST')}")
        return self.get_response(request)
