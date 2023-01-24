from django.urls import path
from .views import network, services, about_us
from .views import home, tracking, contactUs
from .views import login_auth, dashboard, logout, edit_data_retrive
from .views import bookings, tracking_history, save_booking
from .views import advance_search_by_date, advance_search_by_c_note, advance_search_for_ref_number


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
    path(r"advance_search_by_date", advance_search_by_date, name="advance_search_by_date"),     
    path(r"advance_search_by_c_note", advance_search_by_c_note, name="advance_search_by_c_note"),    
    path(r"advance_search_for_ref_number", advance_search_for_ref_number, name="advance_search_for_ref_number"),
]
