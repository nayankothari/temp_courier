from django.urls import path
from .views import advance_search_by_c_note_load_in, edit_party_details, load_in_edit, network, save_parties, services
from .views import delete_party_detail, about_us, tracking_history_in, tracking_history_out
from .views import home, tracking, contactUs
from .views import login_auth, dashboard, logout, edit_data_retrive
from .views import bookings, save_booking, part_master, tracking_with_selenium
from .views import advance_search_by_date, advance_search_by_c_note, advance_search_for_ref_number
from .views import save_input_load, load_in_delete

urlpatterns = [    
    path(r"", home, name="home"),
    path(r"tracking/", home, name="only_tracking"),
    path(r"tracking/<str:tracking_number>", tracking, name="tracking_page"),    
    path(r"tracking/track_internal/<str:details>", tracking_with_selenium),    
    path(r"contact_us", contactUs, name="ContactUS"),    
    path(r"network", network, name="network"),
    path(r"services", services, name="services"),  
    path(r"about_us", about_us, name="about_us"),
    path(r"login_auth", login_auth, name="login_auth"),
    path(r"logout", logout, name="logout"),
    path(r"dashboard", dashboard, name="dashboard"),
    path(r"bookings", bookings, name="bookings"),    
    path(r"save_booking", save_booking, name="save_booking"), 
    path(r"edit_data_retrive", edit_data_retrive, name="edit_data_retrive"),     
    path(r"advance_search_by_date", advance_search_by_date, name="advance_search_by_date"),     
    path(r"advance_search_by_c_note", advance_search_by_c_note, name="advance_search_by_c_note"),    
    path(r"advance_search_for_ref_number", advance_search_for_ref_number, name="advance_search_for_ref_number"),
    path(r"part_master", part_master, name="part_master"),    
    path(r"save_parties", save_parties, name="save_parties"),        
    path(r"edit_party_details", edit_party_details, name="edit_party_details"),        
    path(r"delete_party_detail", delete_party_detail, name="delete_party_detail"),            
    path(r"tracking_history_in", tracking_history_in, name="tracking_history_in"),
    path(r"tracking_history_out", tracking_history_out, name="tracking_history_out"),    
    path(r"save_input_load", save_input_load, name="save_input_load"),
    path(r"delete_input_load", load_in_delete, name="delete_input_load"),    
    path(r"load_in_edit", load_in_edit, name="load_in_edit"),
    path(r"advance_search_by_c_note_load_in", advance_search_by_c_note_load_in, name="advance_search_by_c_note_load_in")

]
