from django.urls import path
from .views import network, services, about_us
from .views import home, tracking, contactUs


urlpatterns = [    
    path(r"", home, name="home"),
    path(r"tracking/", home, name="only_tracking"),
    path(r"tracking/<str:tracking_number>", tracking, name="tracking_page"),    
    path(r"contact_us", contactUs, name="ContactUS"),    
    path(r"network", network, name="network"),
    path(r"services", services, name="services"),  
    path(r"about_us", about_us, name="about_us"),

]
