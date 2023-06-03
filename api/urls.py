from django.urls import path
from django.contrib import admin
from .views import upload_drs_details, print_drs
from .views import advance_search_by_c_note_load_in, advance_search_by_c_note_load_out
from .views import advance_search_by_ref_num_load_in, advance_search_by_ref_num_load_out, advance_search_load_out_by_date
from .views import delivery_boy_master, edit_delivery_boy_details, edit_party_details, load_in_edit
from .views import network, save_delivery_boy_details, save_output_load, save_parties, services
from .views import delete_party_detail, about_us, tracking_history_in, tracking_history_out
from .views import home, tracking, contactUs, save_drs_details, delete_drs_details, upload_drs
from .views import login_auth, dashboard, logout, edit_data_retrive, edit_drs_details
from .views import bookings, save_booking, part_master, tracking_with_selenium, save_edited_drs_details
from .views import advance_search_by_date, advance_search_by_c_note, advance_search_for_ref_number
from .views import save_input_load, load_in_delete, advance_search_load_in_by_date, view_drs
from .views import area_master, save_area_master, edit_area_details, delete_area_detail
from .views import delete_delivery_boy_detail, drs, generate_drs, doc_num_from_booking_to_drs
from .views import manifest_show, search_drs_by_num_date, search_manifest, c_note_master

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
    path(r"advance_search_by_c_note_load_in", advance_search_by_c_note_load_in, name="advance_search_by_c_note_load_in"),
    path(r"advance_search_by_ref_num_load_in", advance_search_by_ref_num_load_in, name="advance_search_by_ref_num_load_in"),
    path(r"advance_search_load_in_by_date", advance_search_load_in_by_date, name="advance_search_load_in_by_date"),     
    path(r"save_output_load", save_output_load, name="save_output_load"),     
    path(r"advance_search_by_c_note_load_out", advance_search_by_c_note_load_out, name="advance_search_by_c_note_load_out"),
    path(r"advance_search_by_ref_num_load_out", advance_search_by_ref_num_load_out, name="advance_search_by_ref_num_load_out"),
    path(r"advance_search_load_out_by_date", advance_search_load_out_by_date, name="advance_search_load_out_by_date"),
    path(r"area_master", area_master, name="area_master"),
    path(r"save_area_master", save_area_master, name="save_area_master"),
    path(r"edit_area_details", edit_area_details, name="edit_area_details"),
    path(r"delete_area_detail", delete_area_detail, name="delete_area_detail"),
    path(r"delivery_boy_master", delivery_boy_master, name="delivery_boy_master"),
    path(r"save_delivery_boy_details", save_delivery_boy_details, name="save_delivery_boy_details"),
    path(r"edit_delivery_boy_details", edit_delivery_boy_details, name="edit_delivery_boy_details"),
    path(r"delete_delivery_boy_detail", delete_delivery_boy_detail, name="delete_delivery_boy_detail"),
    path(r"drs", drs, name="drs"),    
    path(r"drs/generate_drs", generate_drs, name="generate_drs"),    
    path(r"doc_num_from_booking_to_drs", doc_num_from_booking_to_drs, name="doc_num_from_booking_to_drs"),
    path(r"save_drs_details", save_drs_details, name="save_drs_details"),
    path(r"delete_drs_details", delete_drs_details, name="delete_drs_details"),
    path(r"edit_drs_details/<str:drs_number>", edit_drs_details, name="edit_drs_details"),
    path(r"save_edited_drs_details", save_edited_drs_details, name="save_edited_drs_details"),
    path(r"upload_drs/<str:drs_number>", upload_drs, name="upload_drs"),
    path(r"upload_drs_details", upload_drs_details, name="upload_drs_details"),
    path(r"print_drs/<str:drs_number>", print_drs, name="print_drs"),
    path(r"view_drs/<str:drs_number>", view_drs, name="view_drs"),
    path(r"manifest_show", manifest_show, name="manifest_show"),
    path(r"search_drs_by_num_date", search_drs_by_num_date, name="search_drs_by_num_date"),
    path(r"search_manifest", search_manifest, name="search_manifest"),
    path(r"c_note_master", c_note_master, name="c_note_master"),
]

