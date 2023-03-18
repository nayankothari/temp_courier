from django.contrib import admin
from .models import Destination, RefCourier, Booking
from .models import Trackinghistory, ParcelStatus, BranchNetwork
from .models import contactus, State, Token, Country, PartyAccounts
from .models import UserAdditionalDetails, BookingType, DeliveryBoyMaster, AreaMaster

class AdminTracking(admin.ModelAdmin):
    list_display = ['c_note_number', 'in_out_datetime', 'd_from', 'd_to', 'status']

class ContactUs(admin.ModelAdmin):
    list_display = ['name', 'country', 'mobile_number', 'created_at']



admin.site.register(Booking)
admin.site.register(RefCourier)
admin.site.register(Destination)
admin.site.register(Trackinghistory, AdminTracking)
admin.site.register(ParcelStatus)
admin.site.register(BranchNetwork)
admin.site.register(contactus, ContactUs)
admin.site.register(State)
admin.site.register(Token)
admin.site.register(Country)
admin.site.register(PartyAccounts)
admin.site.register(UserAdditionalDetails)
admin.site.register(BookingType)
admin.site.register(DeliveryBoyMaster)
admin.site.register(AreaMaster)
