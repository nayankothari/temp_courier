from django.urls import path
from .views import network, services, about_us
from .views import home, tracking, contactUs
from .views import login_auth, dashboard, logout, edit_data_retrive
from .views import bookings, tracking_history, save_booking


urlpatterns = [    
    path(r"", home, name="home"),
    path(r"tracking/", home, name="only_tracking"),
    path(r"tracking/<str:tracking_number>", tracking, name="tracking_page"),    
    path(r"contact_us", contactUs, name="ContactUS"),    
    path(r"network", network, name="network"),
    path(r"services", services, name="services"),  
    path(r"about_us", about_us, name="about_us"),
    path(r"login_auth", login_auth, name="login_auth"),
    path(r"logout", logout, name="logout"),
    path(r"dashboard", dashboard, name="dashboard"),
    path(r"bookings", bookings, name="bookings"),
    path(r"tracking_history", tracking_history, name="tracking_history"),
    path(r"save_booking", save_booking, name="save_booking"), 
    path(r"edit_data_retrive", edit_data_retrive, name="edit_data_retrive"), 
]
