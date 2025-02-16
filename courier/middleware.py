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
        self.blocked_ips = ['89.248.172.41', '185.234.216.114', '162.216.150.101', '193.41.206.36', '164.92.245.47',
        '157.55.39.52', '159.224.217.252', '176.111.174.153', '57.141.3.21', '57.141.3.13', '150.136.222.122', 
        '124.226.222.66', '146.70.142.134', '45.148.10.237', '78.153.140.93', '34.76.203.56', '212.66.41.21',
        '66.249.75.198', '52.167.144.58', '23.150.248.224', '175.44.42.120', '143.198.114.198', 
        '194.233.82.52', '182.43.70.143', '84.17.49.25', '68.183.80.103', '46.101.84.171', '45.148.10.90',
        '80.85.246.140', '194.38.23.16', '172.203.190.139', '185.180.140.102', '167.71.214.49', '123.207.4.25',
        '196.117.176.103', '8.222.197.183', '47.128.31.182', '66.249.75.199', '47.128.52.140', '139.59.37.23',
        '57.141.3.2', '209.38.210.112', '212.102.33.199', '57.141.3.9', '51.8.102.237', '47.128.44.77', 
        '185.242.226.158', '57.141.3.17', '51.8.102.159', '180.110.203.108', '103.26.10.31', '92.204.144.151',
        '47.128.34.148', '123.57.95.186', '57.141.3.6', '45.156.128.127', '57.141.3.15', '172.203.190.133']  # List of IP addresses to block

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')        
        log.info("Requested IP: {}".format(ip_address))
        if ip_address in self.blocked_ips:
            # You can return a response indicating the IP is blocked
            return HttpResponseForbidden("Site under maintenance.")

        response = self.get_response(request)
        return response

