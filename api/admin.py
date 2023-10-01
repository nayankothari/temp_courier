from django.contrib import admin
from .models import Destination, RefCourier, Booking
from .models import Trackinghistory, ParcelStatus, BranchNetwork
from .models import contactus, State, Token, Country, PartyAccounts, Reasons
from .models import UserAdditionalDetails, BookingType, DeliveryBoyMaster, AreaMaster
from .models import DrsNoGenerator, DrsMaster, DrsTransactionHistory, GstModel, Network
from .models import DrsPermission, Complaints


class AdminTracking(admin.ModelAdmin):
    list_display = ['c_note_number', 'in_out_datetime', 'd_from', 'd_to', 'status']

class ContactUs(admin.ModelAdmin):
    list_display = ['name', 'country', 'mobile_number', 'created_at']

class BookingDetails(admin.ModelAdmin):
    list_display = ["c_note_number", "doc_date", "user", "to_destination",
            "ref_courier_name", "ref_courier_number", "weight", "amount", "booking_mode"]

class AreaDetails(admin.ModelAdmin):
    list_display = ["area_name", "user"]

class BranchDetails(admin.ModelAdmin):
    list_display = ["branch_name", "zone", "contact_person", "pincode","user", "status"]

class DrsDetails(admin.ModelAdmin):
    list_display = ["drs_no", "date", "status", "user"]


class DrspermissionDetails(admin.ModelAdmin):
    list_display = ["user", "can_veiw"]

class DrsTxnHistoryDetails(admin.ModelAdmin):
    list_display = ["docket_number", "drs_number", "origin", "status", "user"]

class DeliveryBoyDetails(admin.ModelAdmin):
    list_display = ["delivery_boy_name", "mobile_number", "alternate_number", "user"]

class DestinationsDetails(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["name"]

class NetworkDetails(admin.ModelAdmin):
    list_display = ["pincode", "user"]

class PartyDetails(admin.ModelAdmin):
    list_display = ["party_name", "mobile_number", "user"]

class UserAddDetails(admin.ModelAdmin):
    list_display = ["user", "alias", "destination", "purchase_date", "licence_expire_date", "is_active"]

class ComplaintsDetails(admin.ModelAdmin):
    list_display = ["doc_number", "created_at","from_counter", "to_counter", "by_user", "status"]


admin.site.register(Booking, BookingDetails)
admin.site.register(RefCourier)
admin.site.register(Destination, DestinationsDetails)
admin.site.register(Trackinghistory, AdminTracking)
admin.site.register(ParcelStatus)
admin.site.register(BranchNetwork, BranchDetails)
admin.site.register(contactus, ContactUs)
admin.site.register(State)
admin.site.register(Token)
admin.site.register(Country)
admin.site.register(PartyAccounts, PartyDetails)
admin.site.register(UserAdditionalDetails, UserAddDetails)
admin.site.register(BookingType)
admin.site.register(DeliveryBoyMaster, DeliveryBoyDetails)
admin.site.register(AreaMaster, AreaDetails)
# admin.site.register(DrsNoGenerator)
admin.site.register(DrsMaster, DrsDetails)
admin.site.register(DrsTransactionHistory, DrsTxnHistoryDetails)
admin.site.register(Reasons)
admin.site.register(GstModel)
admin.site.register(Network, NetworkDetails)
admin.site.register(DrsPermission, DrspermissionDetails)
admin.site.register(Complaints, ComplaintsDetails)