import os
import logging
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseForbidden


log = logging.getLogger(__name__)


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


class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_ips = ['176.111.174.153', '185.234.216.114', '159.224.217.252', '146.70.142.134']  # List of IP addresses to block

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')        
        log.info("Requested IP: {}".format(ip_address))
        if ip_address in self.blocked_ips:
            # You can return a response indicating the IP is blocked
            return HttpResponseForbidden("Site under maintenance.")

        response = self.get_response(request)
        return response

