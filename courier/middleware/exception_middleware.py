from django.shortcuts import render
from django.conf import settings

class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.DEBUG:
            host = "http"
        else:
            # TODO: set for https
            host = "http"

        if response.status_code == 500:
            return render(request, "error_templates/500.html")

        if response.status_code == 404:
            return render(request, "error_templates/404.html")

        if response.status_code == 403:
            return render(request, "error_templates/403.html")

        return response
