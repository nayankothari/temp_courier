from django.db import models
from datetime import datetime
from django.utils import timezone


REF_COURIER_TYPE = (("External", "External"), ("Internal", "Internal"))
OFFICE_NETWORKS = (("Franchise", "Franchise"), ("R O", "R O"))

class State(models.Model):
    state_name = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.state_name

class Token(models.Model):
    token = models.CharField(max_length=500)

    def __str__(self):
        return self.token

class ParcelStatus(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class RefCourier(models.Model):
    name = models.CharField(max_length=500)
    link = models.CharField(max_length=1000)
    type = models.CharField(max_length=50, choices=REF_COURIER_TYPE, default="External")

    def __str__(self):
        return self.name

class Booking(models.Model):
    doc_date = models.DateTimeField(default=datetime.now)    
    c_note_number = models.BigIntegerField(unique=True)    
    from_destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="from_destination", default=1)
    to_destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="to_destination", default=1)
    sender_mobile = models.BigIntegerField()
    receiver_name = models.CharField(max_length=256, null=True, blank=True)
    receiver_mobile_number = models.BigIntegerField()
    ref_courier_name = models.ForeignKey(RefCourier, on_delete=models.CASCADE)
    ref_courier_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.c_note_number)


class Trackinghistory(models.Model):
    c_note_number = models.ForeignKey(Booking, on_delete=models.CASCADE)
    in_out_datetime = models.DateTimeField(default=datetime.now)
    last_updated_datetime = models.DateTimeField(auto_now=True)
    d_from = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="destination_in")
    d_to = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="destination_out")
    status = models.ForeignKey(ParcelStatus, on_delete=models.CASCADE, related_name="status")
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.c_note_number)


class BranchNetwork(models.Model):
    branch_name = models.CharField(max_length=256)
    branch_incharge_number = models.BigIntegerField()
    office_number = models.BigIntegerField(null=True, blank=True)
    office_lane_line_number = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=256, blank=True, null=True)    
    pincode = models.IntegerField()
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=False, blank=False, default="")    
    zone = models.ForeignKey(Destination, on_delete=models.CASCADE)
    area_name = models.CharField(max_length=256, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=256, choices=OFFICE_NETWORKS)

    def __str__(self):
        return self.branch_name


class contactus(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=254)
    country = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, blank=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
