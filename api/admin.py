from django.contrib import admin
from .models import Destination, RefCourier, Booking
from .models import Trackinghistory, ParcelStatus, BranchNetwork

class AdminTracking(admin.ModelAdmin):
    list_display = ['c_note_number', 'in_out_datetime', 'd_from', 'd_to', 'status']



admin.site.register(Booking)
admin.site.register(RefCourier)
admin.site.register(Destination)
admin.site.register(Trackinghistory, AdminTracking)
admin.site.register(ParcelStatus)
admin.site.register(BranchNetwork)


# Register your models here.
