import os
from django.conf import settings
from django.shortcuts import render


class CustomErrorMiddleware:    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return self.handle_404(request)
        elif response.status_code == 500:
            return self.handle_500(request)     
        elif response.status_code == 403:
            return self.handle_404(request)
        
        return response            
        
    def handle_404(self, request):
        # Render and return your custom 404 HTML page            
        return render(request, '404.html', status=404)
        

    def handle_500(self, request):        
        # Render and return your custom 500 HTML page
        return render(request, '500.html', status=500)

        
