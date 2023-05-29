from django.db import models
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


REF_COURIER_TYPE = (("External", "External"), ("Internal", "Internal"))
OFFICE_NETWORKS = (("Franchise", "Franchise"), ("R O", "R O"))
DRS_STATUS = (("Pending", "Pending"), ("Updated", "Updated"))


class Country(models.Model):
    country_name = models.CharField(max_length=256, null=True, blank=False)

    class Meta:
        verbose_name_plural = "Country"

    def __str__(self):
        return self.country_name


class State(models.Model):
    state_name = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        verbose_name_plural = "State"

    def __str__(self):
        return self.state_name


class Token(models.Model):
    token = models.CharField(max_length=500)    
    
    class Meta:
        verbose_name_plural = "Token"

    def __str__(self):
        return self.token


class ParcelStatus(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "Parcel status"

    def __str__(self):
        return self.name


class Destination(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "Destination"

    def __str__(self):
        return self.name

class Reasons(models.Model):
    name = models.CharField(max_length=560, blank=False, null=True)

    class Meta:
        verbose_name_plural = "Reasons"
    
    def __str__(self):
        return self.name    


class PartyAccounts(models.Model):
    party_name = models.CharField(max_length=256, null=True, blank=False)
    mobile_number = models.CharField(max_length=25, null=True, blank=False)
    password = models.CharField(max_length=16, null=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    opening_balance = models.FloatField(blank=True, null=True, default=0.0)    

    class Meta:
        verbose_name_plural = "Party master"

    def __str__(self):
        return self.party_name


class RefCourier(models.Model):
    name = models.CharField(max_length=500)
    link = models.CharField(max_length=1000)
    type = models.CharField(max_length=50, choices=REF_COURIER_TYPE, default="External")
    if_multiple = models.BooleanField(default=True, null=True)
    selenium = models.BooleanField(default=True, null=True)
    multi_name = models.CharField(max_length=350, null=True, blank=True)
    multi_link = models.CharField(max_length=350, null=True, blank=True)
    final_link = models.CharField(max_length=350, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Ref. couriers"

    def __str__(self):
        return self.name
    
class BookingType(models.Model):
    booking_type = models.CharField(max_length=256, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Booking type"

    def __str__(self):
        return str(self.booking_type)


class Booking(models.Model):
    doc_date = models.DateTimeField(default=datetime.now)    
    party_name = models.ForeignKey(PartyAccounts, on_delete=models.CASCADE, null=True, blank=False)
    c_note_number = models.BigIntegerField(unique=True)    
    from_destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="from_destination", default=1)
    to_destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="to_destination", default=1)
    booking_type = models.ForeignKey(BookingType, on_delete=models.CASCADE, related_name="booking_types", null=True, default=1)
    sender_name = models.CharField(max_length=256, null=True, blank=True)
    sender_mobile = models.CharField(max_length=15, blank=True, null=True)
    receiver_name = models.CharField(max_length=256, null=True, blank=True)
    receiver_mobile_number = models.CharField(max_length=256, null=True, blank=False)
    ref_courier_name = models.ForeignKey(RefCourier, on_delete=models.CASCADE)
    ref_courier_number = models.CharField(max_length=50, blank=True)
    weight = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    remarks = models.TextField(max_length=550, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name_plural = "Booking"

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)

    class Meta:
        verbose_name_plural = "Tracking history"

    def __str__(self):
        return str(self.c_note_number)


class BranchNetwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    branch_name = models.CharField(max_length=256)
    branch_incharge_number = models.BigIntegerField()
    office_number = models.BigIntegerField(null=True, blank=True)
    office_lane_line_number = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=256, blank=True, null=True)    
    pincode = models.IntegerField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=False, blank=False, default="")    
    zone = models.ForeignKey(Destination, on_delete=models.CASCADE)
    area_name = models.CharField(max_length=256, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=256, choices=OFFICE_NETWORKS)

    class Meta:
        verbose_name_plural = "Branch network master"

    def __str__(self):  
        return self.branch_name


class contactus(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=254)
    country = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, blank=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        verbose_name_plural = "Contact us"

    def __str__(self):
        return self.name


def new_date():
    expired_date = datetime.now() + timedelta(days=365)
    return expired_date


class UserAdditionalDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    alias = models.CharField(max_length=256, null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(null=True, blank=False, default=True)
    purchase_date = models.DateTimeField(default=datetime.now)    
    licence_expire_date = models.DateTimeField(default=new_date)

    class Meta:
        verbose_name_plural = "User Additional Details"

    def __str__(self):
        return str(self.user.username)


class AreaMaster(models.Model):
    area_name = models.CharField(max_length=350, blank=False, null=True)
    pincode = models.ForeignKey(BranchNetwork, on_delete=models.CASCADE, blank=False, null=True, related_name="pin_code")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True, related_name="user_details")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Area Master"
    
    def __str__(self):
        return self.area_name
    

class DeliveryBoyMaster(models.Model):
    delivery_boy_name = models.CharField(max_length=256, blank=False, null=True)
    mobile_number = models.CharField(max_length=15, blank=False, null=False)
    alternate_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    area_name = models.ForeignKey(AreaMaster, on_delete=models.CASCADE ,blank=False, null=True, related_name="area_names")    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True, related_name="user_detail")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Delivery Boy Details"
    
    def __str__(self):
        return self.delivery_boy_name


class DrsNoGenerator(models.Model):
    drs_number = models.BigIntegerField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        verbose_name_plural = "DRS No. Generator"
    
    def __str__(self):
        return str(self.drs_number)

class DrsMaster(models.Model):
    drs_no = models.CharField(max_length=25, blank=False, null=True)
    date = models.DateTimeField(blank=True, null=True)
    area_name = models.ForeignKey(AreaMaster, on_delete=models.CASCADE ,blank=False, null=True)
    deliveryboy_name = models.ForeignKey(DeliveryBoyMaster, on_delete=models.CASCADE ,blank=False, null=True)
    status = models.CharField(max_length=25, choices=DRS_STATUS, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)    
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "DRS Master"
    
    def __str__(self):
        return self.drs_no


class DrsTransactionHistory(models.Model):
    docket_number = models.CharField(max_length=40, blank=False, null=True)
    origin = models.CharField(max_length=60, blank=True, null=True)
    consignee_name = models.CharField(max_length=256, blank=True, null=True)
    drs_number = models.CharField(max_length=40, blank=True, null=True)    
    status = models.ForeignKey(ParcelStatus, on_delete=models.CASCADE, blank=False, null=True)
    reason = models.TextField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, models.CASCADE, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)    
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "DRS Transaction History"
    
    def __str__(self):
        return self.docket_number