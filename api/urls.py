from django.urls import path
from django.contrib import admin
from .views import *
# from .views import upload_drs_details, print_drs
# from .views import advance_search_by_c_note_load_in, advance_search_by_c_note_load_out
# from .views import advance_search_by_ref_num_load_in, advance_search_by_ref_num_load_out, advance_search_load_out_by_date
# from .views import delivery_boy_master, edit_delivery_boy_details, edit_party_details, load_in_edit
# from .views import network, save_delivery_boy_details, save_output_load, save_parties, services
# from .views import delete_party_detail, about_us, tracking_history_in, tracking_history_out
# from .views import home, tracking, contactUs, save_drs_details, delete_drs_details, upload_drs
# from .views import login_auth, dashboard, logout, edit_data_retrive, edit_drs_details
# from .views import bookings, save_booking, part_master, tracking_with_selenium, save_edited_drs_details
# from .views import advance_search_by_date, advance_search_by_c_note, advance_search_for_ref_number
# from .views import save_input_load, load_in_delete, advance_search_load_in_by_date, view_drs
# from .views import area_master, save_area_master, edit_area_details, delete_area_detail
# from .views import delete_delivery_boy_detail, drs, generate_drs, doc_num_from_booking_to_drs
# from .views import manifest_show, search_drs_by_num_date, search_manifest, c_note_master
# from .views import save_c_note_number, delete_c_note_details, check_tracking_num
# from .views import booking_dashboard, cash_booking, save_cash_booking, edit_cash_booking
# from .views import print_manifest, print_cash_booking, delivery_area_master, save_delivery_area_master_details
# from .views import delete_del_area_master, edit_del_area_master
# from .views import load_out_auto_search_by_date_and_des, load_out_auto_search_by_date_auto


urlpatterns = [    
    path(r"", home, name="home"),
    path(r"tracking/", home, name="only_tracking"),
    path(r"tracking/<str:tracking_number>", tracking, name="tracking_page"),    
    path(r"check_tracking_num", check_tracking_num, name="check_tracking_num"),
    path(r"tracking/track_internal/<str:details>", tracking_with_selenium),    
    
    path(r"contact-us-form", contactUs, name="ContactUS"),   
    path(r"close_contact_us", close_contact_us, name="close_contact_us"), 
    path(r"network", network, name="network"),
    path(r"services", services, name="services"),  
    path(r"about_us", about_us, name="about_us"),
    path(r"terms_and_conditions", terms_and_conditions, name="terms_and_conditions"),
    path(r"privacy_and_policy", privacy_and_policy, name="privacy_and_policy"),
    
    path(r"login_auth", login_auth, name="login_auth"),    
    path(r"logout", logout, name="logout"),
    
    path(r"dashboard", dashboard, name="dashboard"),
    path(r"dashboard_analysis", dashboard_analysis, name="dashboard_analysis"),

    path(r"bulk_print_receipt", bulk_print_receipt, name="bulk_print_receipt"),
    path(r"bulk_print_label", bulk_print_label, name="bulk_print_label"),
    path(r"export_to_excel_bookings", export_to_excel_bookings, name="export_to_excel_bookings"),

    path(r"bookings", bookings, name="bookings"),    
    path(r"save_booking", save_booking, name="save_booking"), 
    path(r"edit_data_retrive", edit_data_retrive, name="edit_data_retrive"),     
    path(r"advance_search_by_date", advance_search_by_date, name="advance_search_by_date"),
    path(r"advance_search_by_c_note", advance_search_by_c_note, name="advance_search_by_c_note"),    
    path(r"advance_search_for_ref_number", advance_search_for_ref_number, name="advance_search_for_ref_number"),
    
    path(r"booking_dashboard", booking_dashboard, name="booking_dashboard"),
    path(r"cash_booking", cash_booking, name="cash_booking"),
    path(r"save_cash_booking", save_cash_booking, name="save_cash_booking"),
    path(r"cash_booking/edit/<str:booking_num>", edit_cash_booking, name="edit_cash_booking"),
    path(r"print_cash_booking/<str:sid>", print_cash_booking, name="print_cash_booking"),
    path(r"advance_date_wise_search_cash_booking", advance_date_wise_search_cash_booking, name="advance_date_wise_search_cash_booking"),
    path(r"advance_date_party_wise_search_cash_booking", advance_date_party_wise_search_cash_booking, name="advance_date_party_wise_search_cash_booking"),
    path(r"advance_c_note_wise_search_cash_booking", advance_c_note_wise_search_cash_booking, name="advance_c_note_wise_search_cash_booking"),
    path(r"advance_date_ref_courier_wise_search_cash_booking", advance_date_ref_courier_wise_search_cash_booking, name="advance_date_ref_courier_wise_search_cash_booking"),

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
    path(r"load_out_auto_search_by_date_and_des", load_out_auto_search_by_date_and_des, name="load_out_auto_search_by_date_and_des"),
    path(r"load_out_auto_search_by_date_auto", load_out_auto_search_by_date_auto, name="load_out_auto_search_by_date_auto"),

    path(r"area_master", area_master, name="area_master"),
    path(r"save_area_master", save_area_master, name="save_area_master"),
    path(r"edit_area_details", edit_area_details, name="edit_area_details"),
    path(r"delete_area_detail", delete_area_detail, name="delete_area_detail"),
    
    path(r"delivery_boy_master", delivery_boy_master, name="delivery_boy_master"),    
    path(r"save_delivery_boy_details", save_delivery_boy_details, name="save_delivery_boy_details"),
    path(r"edit_delivery_boy_details", edit_delivery_boy_details, name="edit_delivery_boy_details"),
    path(r"delete_delivery_boy_detail", delete_delivery_boy_detail, name="delete_delivery_boy_detail"),
    
    path(r"delivery_area_master", delivery_area_master, name="delivery_area_master"),
    path(r"save_delivery_area_master_details", save_delivery_area_master_details, name="save_delivery_area_master_details"),
    path(r"delete_del_area_master", delete_del_area_master, name="delete_del_area_master"),
    path(r"edit_del_area_master", edit_del_area_master, name="edit_del_area_master"),

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
    path(r"search_drs_by_num_date", search_drs_by_num_date, name="search_drs_by_num_date"),

    path(r"manifest_show", manifest_show, name="manifest_show"),
    path(r"search_manifest", search_manifest, name="search_manifest"),
    path(r"print_manifest/<str:sid_num>", print_manifest, name="print_manifesto"),

    path(r"c_note_master", c_note_master, name="c_note_master"),
    path(r"save_c_note_number", save_c_note_number, name="save_c_note_number"),
    path(r"delete_c_note_details", delete_c_note_details, name="delete_c_note_details"),

    path(r"retutn_all_foreign_key_details", retutn_all_foreign_key_details, name="retutn_all_foreign_key_details"),

    path(r"print_barcode_stickers", print_barcode_stickers, name="print_barcode_stickers"),
]

