"""
Some of basic django imports that help to render and filter data from database.
"""
import io
import ast
import csv
import math
import asyncio
import base64
import logging
import pyqrcode
import requests
import datetime
import barcode
from PIL import Image
from .models import Reasons
from django.db.models import F
from django.db.models import Count, Sum
from datetime import timedelta
from django.db.models import Max
from django.contrib import messages
from barcode.writer import SVGWriter
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Q, Count
from .test_api import get_search_details
from django.shortcuts import render, redirect
from django.db.models.functions import Substr
from django.contrib.auth.models import User, auth
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import CNoteGenerator, State, GstModel, Network
from .models import contactus, Token, BranchNetwork, Destination
from .models import DrsNoGenerator, DrsMaster, DrsTransactionHistory, UserBooking
from .models import RefCourier, PartyAccounts, AreaMaster, DeliveryBoyMaster
from .models import Booking, BookingType, ParcelStatus, Trackinghistory, UserAdditionalDetails
from .models import DrsPermission, Complaints, MessageMarquee
from django.db.models.functions import TruncDate
from django.db import connection


BARCODE_CLASS = barcode.get_barcode_class("code128")
log = logging.getLogger(__name__)
today_date = datetime.datetime.now().strftime("%Y")

def get_marque_message():
    message = MessageMarquee.objects.all()
    if message.exists():
        return message[0]
    return None

# Create your views here.
def home(request):  
    """
    Thi function returns to home page.
    """         
    if request.method == "POST":
        tracking_id = request.POST.get("tracking_number")                
        if tracking_id:                                    
            return redirect("/tracking/{}".format(tracking_id))    
    MARQUE_MESSAGE = get_marque_message()
    return render(request, "index.html", {"today_date": today_date, "return_message": None, "marque_message": MARQUE_MESSAGE})    


def tracking(request, tracking_number):    
    tracking_number_drs = tracking_number
    try:        
        tracking_number = int(tracking_number)  
        client_ip = request.META.get('REMOTE_ADDR', "Not available")
        log.info("Search for tracking number: {} by user {} by IP: {}".format(tracking_number, request.user, client_ip))     
        if tracking_number:
            data = Booking.objects.filter(c_note_number=tracking_number)                        
            comp_details = Complaints.objects.filter(doc_number=tracking_number).order_by("-created_at")
            comp_exists = 0
            show_comp_button = 1
            if comp_details.exists():
                comp_exists = 1
                if (len(comp_details) % 2):
                    show_comp_button = 0                                
            if data.exists():                                
                booking_details = data[0]                                    
                tracking_history = Trackinghistory.objects.filter(c_note_number=booking_details).order_by('-in_out_datetime')                
                # print(booking_details.c_note_number, booking_details.from_destination,
                # booking_details.to_destination, booking_details.doc_date.strftime("%d-%b-%Y %H:%M %p"), booking_details.receiver_name)                                    
                if_drs = None
                last_status = "Shipment Booked by Airpost xpress"
                if tracking_history.exists():                    
                    last_status = str(tracking_history[0].status) + " - " + str(tracking_history[0].d_to)

                if booking_details.ref_courier_name.type != 'Internal':
                    tracking_history = {}
                    token_obj = Token.objects.all().values()
                    token = ""
                    if token_obj:
                        token = token_obj[0]["token"]
                    url = str(booking_details.ref_courier_name.link).format(token) + str(booking_details.ref_courier_number)                    
                    try:
                        response = requests.post(url, headers={"content-type": "application/json"}, timeout=2)
                        data_load_from_another_site = response.json()                    
                        last_status = data_load_from_another_site.get("MostRecentStatus", "-")
                        tracking_history = data_load_from_another_site.get("Checkpoints", "")                    
                        if len(tracking_history) <= 2:
                            for i in tracking_history:                            
                                if str(i.get("Activity")).__contains__("No information present for consignment"):                      
                                    tracking_history = tracking_history[0]                                                                                     
                                    int("a")      
                                                  
                    except Exception as e:                                                
                        selenium = False
                        if booking_details.ref_courier_name.if_multiple:                                                                                    
                            url = booking_details.ref_courier_name.multi_link
                            url = url.format(booking_details.ref_courier_number)                            
                        else:                                                                                 
                            if booking_details.ref_courier_name.selenium:
                                selenium = True
                                url = str(booking_details.ref_courier_name.multi_name) + "UUUU" + str(booking_details.ref_courier_number)

                        if selenium:                            
                            # booking_details.c_note_number
                            url = f'<a id="sele_data" class="sele_data_1 btn btn-outline-primary btn-sm text-dark" data-sid="{url}" >Get current status <i class="bi bi-arrow-clockwise"></i></a>'
                        else:
                            url = f'<a href="{url}" target="_blank" class="btn btn-outline-primary btn-sm text-dark">Get current status <i class="bi bi-arrow-clockwise"></i></a>'
                        tracking_history["Date"] = ""
                        tracking_history["Location"] = ""
                        tracking_history["CheckpointState"] = ""
                        tracking_history["Activity"] = url
                        tracking_history = [tracking_history,]
                
                else:                    
                    final_status = DrsTransactionHistory.objects.filter(docket_number=tracking_number).order_by("-created_at")
                    if final_status.exists():
                        final_status = final_status[0] 
                        drs_num = final_status.drs_number                                           
                        delivery_boy_detail = DrsMaster.objects.get(drs_no=final_status.drs_number, user=final_status.user)
                        delivery_boy_detail = delivery_boy_detail.deliveryboy_name                        
                        if_drs = 1                        
                        last_status = final_status.status       
                        reason = ""
                        if final_status.reason:
                            reason = final_status.reason     

                        MARQUE_MESSAGE = get_marque_message()
                        return render(request, "tracking.html", {"booking_details": booking_details, "tracking_history": tracking_history,
                    "last_status": last_status, "today_date": today_date, "drs_details": if_drs, 
                    "status": final_status.status, "reason": reason, "date": final_status.created_at,
                      "dbd": delivery_boy_detail, "drs_num": drs_num,"comp_details": comp_details, "comp_exists": comp_exists, "show_comp_button": show_comp_button, "marque_message": MARQUE_MESSAGE})
                MARQUE_MESSAGE = get_marque_message()
                return render(request, "tracking.html", {"booking_details": booking_details, "tracking_history": tracking_history,
                "last_status": last_status, "today_date": today_date, "drs_details": if_drs, "comp_details": comp_details, "comp_exists": comp_exists, "show_comp_button": show_comp_button, "marque_message": MARQUE_MESSAGE})   
            
            else: # use for internal drs tracking
                if request.user.is_authenticated:
                    drs_permission = DrsPermission.objects.filter(user=request.user, can_veiw=True)
                    if drs_permission.exists():
                        # drs_obj = DrsTransactionHistory.objects.filter(user=request.user, docket_number=tracking_number).order_by("-created_at")                                        
                        drs_obj = DrsTransactionHistory.objects.filter(docket_number=tracking_number_drs).order_by("-created_at")                    
                        if drs_obj.exists():
                            # find booking complaint
                            comp_exists = 0
                            show_comp_button = 0
                            if_drs = 1    
                            only_and_only_drs = 1 
                            final_status = drs_obj[0]                          
                            drs_num = final_status.drs_number   
                            delivery_boy_detail = DrsMaster.objects.get(drs_no=final_status.drs_number, user=final_status.user)
                            delivery_boy_detail = delivery_boy_detail.deliveryboy_name                                                                 
                            last_status = final_status.status                               
                            reason = ""                        
                            if final_status.reason:
                                reason = final_status.reason
                            MARQUE_MESSAGE = get_marque_message()
                            return render(request, "tracking.html", {"tracking_history": [],
                        "last_status": last_status, "today_date": today_date, "drs_details": if_drs, "status": final_status.status, 
                        "reason": reason, "date": final_status.created_at, "only_and_only_drs": only_and_only_drs,
                        "c_note_number": tracking_number, "from_destination": final_status.origin, "receiver_name": final_status.consignee_name,
                        "dbd": delivery_boy_detail, "drs_num": drs_num,"comp_exists": comp_exists, "show_comp_button": show_comp_button, "marque_message": MARQUE_MESSAGE})

        return redirect("home")        
    except Exception as e:   
        if request.user.is_authenticated:            
            drs_permission = DrsPermission.objects.filter(user=request.user, can_veiw=True)
            if drs_permission.exists():
                # drs_obj = DrsTransactionHistory.objects.filter(user=request.user, docket_number=tracking_number).order_by("-created_at")                                        
                tracking_number = str(tracking_number_drs)                              
                drs_obj = DrsTransactionHistory.objects.filter(docket_number=tracking_number).order_by("-created_at")                    
                if drs_obj.exists():
                    # find booking complaint
                    comp_exists = 0
                    show_comp_button = 0
                    if_drs = 1    
                    only_and_only_drs = 1 
                    final_status = drs_obj[0]                             
                    drs_num = final_status.drs_number     
                    delivery_boy_detail = DrsMaster.objects.get(drs_no=final_status.drs_number, user=final_status.user)
                    delivery_boy_detail = delivery_boy_detail.deliveryboy_name                                                                 
                    last_status = final_status.status                               
                    reason = ""                        
                    if final_status.reason:
                        reason = final_status.reason
                    MARQUE_MESSAGE = get_marque_message()
                    return render(request, "tracking.html", {"tracking_history": [],
                "last_status": last_status, "today_date": today_date, "drs_details": if_drs, "status": final_status.status, 
                "reason": reason, "date": final_status.created_at, "only_and_only_drs": only_and_only_drs,
                "c_note_number": tracking_number, "from_destination": final_status.origin, "receiver_name": final_status.consignee_name,
                "dbd": delivery_boy_detail, "drs_num": drs_num, "comp_exists": comp_exists, "show_comp_button": show_comp_button, "marque_message": MARQUE_MESSAGE})            
        log.exception(e)
        log.info("Error for finding tracking number: {}".format(tracking_number))        
        return redirect("home")

def check_tracking_num(request):
    if request.method == "POST":
        try:
            tracking_num = request.POST.get("tracking_num")
            if str(tracking_num).strip():
                try:
                    data = Booking.objects.filter(c_note_number=tracking_num)                        
                    if data.exists():
                        return JsonResponse({"status": 1})
                    elif request.user.is_authenticated:
                        drs_permission = DrsPermission.objects.filter(user=request.user, can_veiw=True)
                        if drs_permission.exists():
                            drs_obj = DrsTransactionHistory.objects.filter(docket_number=tracking_num).order_by("-created_at")
                            if drs_obj.exists():                                
                                return JsonResponse({"status": 1})    
                        else:                        
                            return JsonResponse({"status": 0, "message": "DRS Details not available."})            
                except:
                    if request.user.is_authenticated:
                        drs_permission = DrsPermission.objects.filter(user=request.user, can_veiw=True)
                        if drs_permission.exists():
                            drs_obj = DrsTransactionHistory.objects.filter(docket_number=tracking_num).order_by("-created_at")
                            if drs_obj.exists():                                
                                return JsonResponse({"status": 1})    
                        else:                        
                            return JsonResponse({"status": 0, "message": "DRS Details not available."})
            return JsonResponse({"status": 0, "message": "Insert Correct docket Number"})
        except Exception as e:
            log.exception(e)
    return JsonResponse({"status": 0, "message": "Insert Correct docket Number"})

def tracking_with_selenium(request, details):
    # def start_in_thread():
    final_data = str(details).split("UUUU")
    courier = final_data[0]
    doc_number = final_data[1]    
    data = get_search_details(courier=courier, doc_number=doc_number)

    return JsonResponse({"status": 1, "data": data})
    # threading.Thread(target=start_in_thread).start()

# ############################# Reg New Complaint ####################################
def save_commplaint(request):
    if request.method == "POST":
        try:
            message = str(request.POST.get("message")).strip()
            if message:
                doc_num = request.POST.get("c_note_nmber")        
                booking_obj = Booking.objects.filter(c_note_number=int(doc_num))
                if booking_obj.exists():
                    from_user = booking_obj[0].user
                    to_dest = booking_obj[0].to_destination                                                 
                    to_brn = BranchNetwork.objects.filter(zone=to_dest)                    
                    if to_brn.exists():
                        to_brn = to_brn[0].user                        
                    else:
                        to_brn = from_user                    
                    Complaints(message=message, status="OPEN", by_user="CLIENT", to_counter=to_brn,
                            from_counter=from_user, doc_number=int(doc_num)).save()                            
                    return JsonResponse({"status": 1})
                else:
                    return JsonResponse({"status": 0, "message": "Shipment Not found."})
            else:
                return JsonResponse({"status": 0, "message": "Insert Message."})
                
        except Exception as e:
            log.exception(e)
    return JsonResponse({"status": 0, "message": "Get method not allowed."})


def update_compliant_by_counter(request):
    if request.method == "POST":
        try:
            doc_num = request.POST.get("doc_n")
            doc_num = int(doc_num)
            message = request.POST.get("message")
            doc_details = Complaints.objects.filter(doc_number=doc_num).update(status="RESOLVED")
            if not doc_details:
                return JsonResponse({"status": 0, "message": "Complaint not found for this shipment number."})
            user = request.user
            Complaints(message=message, status="CLOSE", by_user="COUNTER", to_counter=user,
                        from_counter=user, doc_number=doc_num).save()
            return JsonResponse({"status": 1})                
        except Exception as e:
            log.exception(e)
            return JsonResponse({"status": 0, "message": "Complaint not found for this shipment number."})
    return JsonResponse({"status": 0, "message": "Get method not allowed."})

# @login_required(login_url="login_auth")
def get_complaints(request):
    if request.user.is_authenticated:
        user = request.user            
        if user.is_superuser:            
            complaints = Complaints.objects.filter(status="OPEN").order_by("created_at").values("doc_number",
                    "created_at", "message")
        else:            
            complaints = Complaints.objects.filter((Q(from_counter=user) |
            Q(to_counter=user)) & Q(status="OPEN")).order_by("created_at").values("doc_number",
                    "created_at", "message")    
            
        for complaint in complaints:
            complaint["created_at"] = complaint["created_at"].strftime("%Y-%m-%d %I:%M:%S %p")
        return JsonResponse({"status": 1, "complaints": list(complaints)})
    
    log.critical(f"{request.user} Someone wants to access complaints without permission.")
    return JsonResponse({"status": "Authentication failed: Action recorded and share with admin."})

# ################################ Contact us #######################################
def contactUs(request):    
    try:
        if request.method == "POST":                    
            name = request.POST.get("name")
            email = request.POST.get("email")
            country = request.POST.get("country")
            pincode = request.POST.get("pincode")
            message = request.POST.get("message")        
            exclude_names = ["RobertTiz", "RaymondTum"]
            if str(name) not in exclude_names:
                if name and email and country and pincode:            
                    contact_obj = contactus.objects.create(name=name, email=email, country=country,
                                    mobile_number=pincode, message=message, status="OPEN")
                    contact_obj.save()
                    return_message = "Request submitted successfully."       
                    MARQUE_MESSAGE = get_marque_message()
                    client_ip = request.META.get('REMOTE_ADDR', "Not Available")
                    log.warning(f"saved contact info by Form name: {str(name)} and contact details, By : logged-in user name: {request.user} and IP: {client_ip}")
                    return render(request, "contactus.html", {"return_message": return_message, "today_date": today_date, "marque_message": MARQUE_MESSAGE})                    
            else:
                client_ip = request.META.get('REMOTE_ADDR')
                log.info("RobertTiz IP : {}".format(client_ip))            
    except Exception as e:
        log.exception(e)
        
    MARQUE_MESSAGE = get_marque_message()
    client_ip = request.META.get('REMOTE_ADDR', "Not Available")
    log.warning(f"Getting contact details, {request.user} by IP: {client_ip}")
    return render(request, "contactus.html", {"today_date": today_date, "marque_message": MARQUE_MESSAGE})

def network(request):
    message = 1    
    head_offices = BranchNetwork.objects.filter(status="R O")[:50]
    try:           
        if request.method == "POST":
            if "by_pincode" in request.POST and request.POST.get("pincode"):
                try:
                    pincode = int(request.POST.get("pincode"))
                    if len(str(pincode)) == 6:
                        data = BranchNetwork.objects.filter(pincode=pincode)                                             
                        if data:        
                            add_details = Network.objects.filter(user=data[0].user)                                                          
                            message = None                                                                        
                            context = {"head_offices": head_offices, "message": None,
                                        "data": data, "today_date": today_date, "add_details": add_details, 
                                        "by_pincode": 1}
                            return render(request, "network.html", context=context)
                        
                        add_details = Network.objects.filter(pincode=pincode)                    
                        if add_details.exists():
                            data = BranchNetwork.objects.filter(user=add_details[0].user)
                            context = {"head_offices": head_offices, "message": None, "today_date": today_date, 
                                    "data": data, "add_details":add_details, "by_pincode": 1}
                            return render(request, "network.html", context=context)
                        else:                        
                            context = {"head_offices": head_offices, "message": 1, "today_date": today_date, "by_pincode": 1}
                            return render(request, "network.html", context=context)
                    else:
                        context = {"head_offices": head_offices, "message": 1, "today_date": today_date}
                        return render(request, "network.html", context=context) 
                except Exception as e:
                    log.exception(e)
            elif "by_area" in request.POST and request.POST.get("area_name"):
                area_name = request.POST.get("area_name")           
                ques = (Q(branch_name__icontains=area_name) | Q(state__state_name__icontains=area_name) 
                | Q(zone__name__icontains=area_name) | Q(area_name__icontains=area_name))
                data = BranchNetwork.objects.filter(ques)[:25]
                if data:                                              
                    message = None
                    context = {"head_offices": head_offices, "message": None, "data": data, "today_date": today_date}
                    return render(request, "network.html", context=context)
                else:
                    context = {"head_offices": head_offices, "message": 1, "today_date": today_date}
                    return render(request, "network.html", context=context)            
            
            else:
                context = {"head_offices": head_offices, "message": 1, "today_date": today_date}
                return render(request, "network.html", context=context)
    except Exception as e:
        log.exception(e)
    message = None
    MARQUE_MESSAGE = get_marque_message()
    context = {"head_offices": head_offices, "message": message, "today_date": today_date, "marque_message": MARQUE_MESSAGE}
    return render(request, "network.html", context=context)


def terms_and_conditions(request):
    MARQUE_MESSAGE = get_marque_message()
    context = {"marque_message": MARQUE_MESSAGE}
    return render(request, "terms_and_condition/terms_and_condition.html", context=context)

def privacy_and_policy(request):
    MARQUE_MESSAGE = get_marque_message()
    return render(request, "terms_and_condition/privacy_and_policy.html", context={"marque_message": MARQUE_MESSAGE})

def services(request):
    MARQUE_MESSAGE = get_marque_message()
    return render(request, "services.html", context={"today_date": today_date, "marque_message": MARQUE_MESSAGE})


def about_us(request):
    MARQUE_MESSAGE = get_marque_message()
    return render(request, "aboutus.html", context={"today_date": today_date, "marque_message": MARQUE_MESSAGE})


def login_auth(request):
    try:
        if request.method == "POST":
            user_name = request.POST.get("username")
            password = request.POST.get("password")
            user = auth.authenticate(username=user_name, password=password)
            if user:
                license_exp_date = UserAdditionalDetails.objects.get(user=user).licence_expire_date
                remaining_time = (license_exp_date - datetime.datetime.now()).days            
                if not remaining_time <= 0:
                    auth.login(request, user)
                    log.info(f"Successfully login by user: {user_name}")
                    return redirect("dashboard")
                
                context = {"message": "Your license is expired, please connect with support team", "today_date": today_date}
                log.warning(f"Licence expired for user: {user_name}")
                return render(request, "login.html", context)
            else:
                log.error(f"{user_name} try to login with password: {password}, but failed.")
                MARQUE_MESSAGE = get_marque_message()
                context = {"message": "Invalid credentials !", "today_date": today_date, "marque_message": MARQUE_MESSAGE}
                return render(request, "login.html", context)
    except Exception as e:
        log.exception(e)
    MARQUE_MESSAGE = get_marque_message()
    return render(request, "login.html", context={"today_date": today_date, "marque_message": MARQUE_MESSAGE})


@login_required(login_url="login_auth")
def logout(request):
    auth.logout(request)
    return redirect("login_auth")

# ########################### Main Dashboard Detaiuls ##########################
@login_required(login_url="login_auth")
def dashboard(request):    
    from_date = datetime.datetime.now().strftime("%Y-%m-%d")
    to_date = datetime.datetime.now().strftime("%Y-%m-%d")
    MARQUE_MESSAGE = get_marque_message()
    return render(request, "dashboard.html", context={"from_date": from_date, "to_date": to_date, "marque_message": MARQUE_MESSAGE})


@login_required(login_url="login_auth")
def dashboard_analysis(request):    
    try:
        if request.method == "POST":        
            from_date = request.POST.get("from_date")
            to_date = request.POST.get("to_date")        

            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")        
            
            today_date = to_date + timedelta(days=1)        
            
            final_result = {}
            # Booking result
            total_bookings = Booking.objects.filter(user=request.user, doc_date__range=(from_date, today_date)).aggregate(total_bookings=Count('id'),total_amount=Sum('amount'))
            final_result["total_booking"] = total_bookings        
            party_booking = Booking.objects.filter(user=request.user, doc_date__range=(from_date, today_date), booking_mode="A/C").aggregate(total_bookings=Count('id'),total_amount=Sum('amount'))
            final_result["party_booking"] = party_booking

            cash_booking = Booking.objects.filter(user=request.user, doc_date__range=(from_date, today_date)).exclude(booking_mode="A/C").aggregate(total_bookings=Count('id'),total_amount=Sum('amount'))
            final_result["cash_booking"] = cash_booking

            # Load IN-OUT result
            status = ParcelStatus.objects.get(name="OUT")
            load_out = Trackinghistory.objects.filter(user=request.user, in_out_datetime__range=(from_date, today_date), status=status).count()
            status = ParcelStatus.objects.get(name="IN")
            load_in = Trackinghistory.objects.filter(user=request.user, in_out_datetime__range=(from_date, today_date), status=status).count()
            final_result["load_out"] = load_out
            final_result["liad_in"] = load_in
            # DRS result
            drs_details = DrsMaster.objects.filter(user=request.user, date__range=(from_date, today_date)).values("status").annotate(count=Count("status"))
            drs_data = []        
            for i in drs_details:
                drs_data_dic = {}
                drs_data_dic["status"] = i["status"]
                drs_data_dic["count"] = i["count"]
                drs_data.append(drs_data_dic)
            final_result["drs_details"] = drs_data

            # Courier wise count
            courier_wise_details = Booking.objects.filter(user=request.user, doc_date__range=(from_date, today_date)).values("ref_courier_name__name").annotate(count=Count("ref_courier_name__name")).order_by("-count")
            courier_data = []        
            for i in courier_wise_details:
                courier_data_dic = {}
                courier_data_dic["name"] = i["ref_courier_name__name"]
                courier_data_dic["count"] = i["count"]
                courier_data.append(courier_data_dic)
            final_result["courier_data"] = courier_data

            # Party wise details
            party_wise_booking = Booking.objects.filter(user=request.user, doc_date__range=(from_date, today_date), booking_mode="A/C").values("party_name__party_name").annotate(count=Count("party_name__party_name")).order_by("-count")
            courier_data = []        
            for i in party_wise_booking:
                courier_data_dic = {}
                courier_data_dic["name"] = i["party_name__party_name"]
                courier_data_dic["count"] = i["count"]
                courier_data.append(courier_data_dic)
            final_result["party_wise_breakup"] = courier_data

            # Booking type wise details
            booking_type_wise = Booking.objects.filter(user=request.user, doc_date__range=(from_date, today_date)).values("booking_type__booking_type").annotate(count=Count("booking_type__booking_type")).order_by("-count")
            courier_data = []        
            for i in booking_type_wise:
                courier_data_dic = {}
                courier_data_dic["name"] = i["booking_type__booking_type"]
                courier_data_dic["count"] = i["count"]
                courier_data.append(courier_data_dic)
            final_result["booking_type_wise"] = courier_data        

            # Contact us details.
            if request.user.is_superuser:
                con_us_details = contactus.objects.filter(created_at__range=(from_date, today_date)).order_by("-created_at").values()
                final_result["contact_us"] = list(con_us_details)                    
            return JsonResponse({"status": 1, "data": final_result})
    except Exception as e:
        log.exception(e)

    return JsonResponse({"status": 0})


# ############################### Print baecode stickers ###############################
@login_required(login_url="login_auth")
def print_barcode_stickers(request):
    def generate_barcode(bcd):
        barcode_class = barcode.get_barcode_class("code128")
        barcode_svg = barcode_class(bcd)
        barcode_svg_ren = barcode_svg.render(writer_options={"module_width": float(.4), "module_height": float(5),
                                                             "font_size": 12, "text_distance": 4, "quite_zone": 3}).decode("utf-8")
        barcode_svg_ren = barcode_svg_ren.replace('<text', '<text style="font-weight: bold; text-anchor: middle;"')
        return barcode_svg_ren
    group_in_one = 2
    test_list = []
    for i in range(2121111, 2121112 + 1):
        res = generate_barcode(str(i))
        test_list.append(res)
    
    total_round = math.ceil(len(test_list)/group_in_one)
    counter = 0
    final_result = []
    for i in range(total_round):
        sublist = test_list[counter: counter + group_in_one]
        final_result.append(sublist)
        counter += group_in_one
    
    # multi_index = True
    # if group_in_one <= 1:
    #     multi_index = False    
    return render(request, "print_barcode/print_barcode.html", context={"bcd": final_result})


# ###############################3 Dashboard details #####################################

@login_required(login_url="login_auth")
def booking_dashboard(request):
    parties = PartyAccounts.objects.filter(user=request.user).order_by("party_name")
    today_date = datetime.date.today()    
    today_bookings = {} # Booking.objects.filter(created_at__startswith=today_date, user=request.user).order_by("-created_at")    
    ref_couriers = RefCourier.objects.all()
    context = {
        "todays_booking": today_bookings,
        "parties": parties,
        "ref_couriers": ref_couriers
    }
    return render(request, "booking_dashboard.html", context=context)


@login_required(login_url="login_auth")
def booking_dashboard_return(request):
    if request.method == "POST":
        today_date = datetime.date.today()    
        today_bookings = Booking.objects.filter(created_at__startswith=today_date, 
                                user=request.user).order_by("-created_at").values("id",
                        "c_note_number", "doc_date", "to_destination__name", "booking_type__booking_type",
                        "party_name__party_name", "receiver_name", "weight", "freight_charge", "amount", 
                        "ref_courier_name__name", "booking_mode")  
                        
        return JsonResponse({"status": 1, "data": list(today_bookings)})
    return JsonResponse({"status": 0})

@login_required(login_url="login_auth")
def export_to_excel_bookings(request):
    try:
        if request.method == "POST":
            list_of_c_notes = request.POST.getlist("export_to_excel_input")
            list_of_c_notes = list_of_c_notes[0]
            list_of_c_notes = ast.literal_eval(list_of_c_notes)
            booking_details = Booking.objects.filter(user=request.user, 
                c_note_number__in=list_of_c_notes).order_by("ref_courier_number")
            if booking_details.exists():      
                file_name = datetime.datetime.now().strftime("Booking_%Y-%m-%d %I:%M.csv")
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                
                writer = csv.writer(response)
                writer.writerow(["C. Note number", "Booking date", "To destination", "Booking type", "Party name",
                    "Sender name", "Receiver name", "Weight in (G.)", "Ref. Courier name", "Ref. Number"])

                for obj in booking_details:
                    writer.writerow([obj.c_note_number, obj.doc_date, 
                                    obj.to_destination, obj.booking_type, obj.party_name, obj.sender_name,
                                    obj.receiver_name, obj.weight, obj.ref_courier_name, "'" + str(obj.ref_courier_number)])
                return response
            return redirect("booking_dashboard")
        return redirect("booking_dashboard")
    except Exception as e:
        log.exception(e)
        return redirect("booking_dashboard")


@login_required(login_url="login_auth")
def close_contact_us(request):
    try:
        if request.method == "POST":
            sid = request.POST.get("sid")
            try:
                details = contactus.objects.get(id=sid)
                details.status = "RESOLVED"
                details.save()
                return JsonResponse({"status": 1})
            except Exception as e:            
                log.exception(e)
                return JsonResponse({"status": 0, "message": "Details not found."})    
    except Exception as e:
        log.exception(e)

    return JsonResponse({"status": 0, "message": "Get request not allowed."})

# ############################# Bulk label or receipt prints #########################

@login_required(login_url="login_auth")
def bulk_print_receipt(request):
    if request.method == "POST":
        list_of_c_notes = request.POST.getlist("receipt_input")                
        try:
            def generate_bulk_bcd(li_c_notes):
                barcode_list = {}
                for i in li_c_notes:
                    barcode_svg = BARCODE_CLASS(str(i)).render(writer_options={"module_width": float(.29),
                                                    "module_height": float(6), "write_text": False}).decode("utf8")   
                    barcode_list["barcode"] = barcode_svg
                    break
                return barcode_list
            
            list_of_c_notes = list_of_c_notes[0]
            list_of_c_notes = ast.literal_eval(list_of_c_notes)                        
            barcode_details = generate_bulk_bcd(list_of_c_notes)     
            qr_url = (f"https://airpostxpress.com/")
            qr_code = pyqrcode.create(qr_url)                
            svg_buffer = io.BytesIO()
            qr_code.svg(svg_buffer, scale=10, module_color='#000', background='#fff')
            svg_buffer.seek(0)        
            svg_base64 = base64.b64encode(svg_buffer.getvalue()).decode()        
            qr_code = f'<img src="data:image/svg+xml;base64,{svg_base64}" width="90" height="90" alt="QR Code">'
            booking_details = Booking.objects.filter(user=request.user, c_note_number__in=list_of_c_notes)        
            user_details = BranchNetwork.objects.get(user=request.user)
            if booking_details.exists():
                steps = math.ceil(len(booking_details) / 4)
                counter = 0
                result = []
                for _ in range(steps):                
                    result.append(booking_details[counter: counter + 4])
                    counter += 4                
                return render(request, "bulk_receipt_print.html", context={"booking_details": result, 
                                                        "bcd": barcode_details, "ud": user_details, "qr_code": qr_code})
        except Exception as e:
            log.exception(e)         
            return redirect("booking_dashboard")    
    return redirect("booking_dashboard") 


@login_required(login_url="login_auth")
def bulk_print_label(request):
    if request.method == "POST":
        list_of_c_notes = request.POST.getlist("lbl_input")                
        try:
            def generate_bulk_bcd(li_c_notes):
                barcode_list = {}
                for i in li_c_notes:
                    barcode_svg = BARCODE_CLASS(str(i)).render(writer_options={"module_width": float(.29),
                                                    "module_height": float(6), "write_text": False}).decode("utf8")   
                    barcode_list["barcode"] = barcode_svg
                    break
                return barcode_list
            
            list_of_c_notes = list_of_c_notes[0]
            list_of_c_notes = ast.literal_eval(list_of_c_notes)                        
            barcode_details = generate_bulk_bcd(list_of_c_notes)     
            qr_url = (f"https://airpostxpress.com/")
            qr_code = pyqrcode.create(qr_url)                
            svg_buffer = io.BytesIO()
            qr_code.svg(svg_buffer, scale=10, module_color='#000', background='#fff')
            svg_buffer.seek(0)        
            svg_base64 = base64.b64encode(svg_buffer.getvalue()).decode()        
            qr_code = f'<img src="data:image/svg+xml;base64,{svg_base64}" width="90" height="90" alt="QR Code">'
            booking_details = Booking.objects.filter(user=request.user, c_note_number__in=list_of_c_notes)        
            user_details = BranchNetwork.objects.get(user=request.user)
            if booking_details.exists():
                steps = math.ceil(len(booking_details) / 4)
                counter = 0
                result = []
                for _ in range(steps):                
                    result.append(booking_details[counter: counter + 4])
                    counter += 4                
                return render(request, "bulk_label_print.html", context={"booking_details": result, 
                                                        "bcd": barcode_details, "ud": user_details, "qr_code": qr_code})
        except Exception as e:
            log.exception(e)      
            return redirect("booking_dashboard")    
    return redirect("booking_dashboard") 

# ############################# Cash Booking details ##############################

@login_required(login_url="login_auth")
def cash_booking(request):
    context = {}
    try:
        booking_type = BookingType.objects.all()
        ref_courier_name = RefCourier.objects.all()
        from_destination = UserAdditionalDetails.objects.get(user=request.user)    
        # destinations = Destination.objects.all()    
        states = State.objects.all()
        gst_rates = GstModel.objects.all()        
        context = {"ref_courier_names": ref_courier_name,               
                "booking_type": booking_type,                
                "from_destination": from_destination,
                "states": states, "gst_rates": gst_rates} 
    except Exception as e:
        log.exception(e)

    return render(request, "cash_booking.html", context=context)

@login_required(login_url="login_auth")
def save_cash_booking(request):
    if request.method == "POST":        
        try:
            c_note_number = int(request.POST.get("c_note_no"))
            request.session["success"] = None
            process_further = False
            c_note_details = CNoteGenerator.objects.filter(user=request.user)
            for i in c_note_details:            
                if int(i.from_range) <= int(c_note_number) <= int(i.to_range):
                    process_further = True 
                    break                            
            
            if process_further:
                update_id = request.POST.get("id_of")                              
                existing_c_note = Booking.objects.filter(c_note_number=c_note_number)                            
                booking_type = request.POST.get("booking_type")                       
                booking_type = BookingType.objects.get(id=int(booking_type))                  
                booking_datetime = request.POST.get("datetime") 
                payment_mode = request.POST.get("payment_mode")
                ref_courier_name = request.POST.get("ref_courier_name")        
                ref_courier_name = RefCourier.objects.get(id=ref_courier_name)
                ref_number = request.POST.get("ref_number")                
                sender_name = request.POST.get("sender_name")
                sender_mobile = request.POST.get("sender_mobile")
                sender_address = request.POST.get("sender_address")
                from_destination = request.POST.get("from_destination")            
                from_destination = Destination.objects.get(id=from_destination)
                gst_number = request.POST.get("gst_number")
                e_way_bill = request.POST.get("e_way_bill")
                receiver_name = request.POST.get("receiver_name")
                receiver_mobile = request.POST.get("receiver_mobile")        
                receiver_address = request.POST.get("receiver_address")
                to_destination = request.POST.get("to_destination")            
                to_destination = Destination.objects.get(id=to_destination)
                pincode = request.POST.get("pincode")
                state = request.POST.get("state")
                state = State.objects.get(id=state)
                qty = request.POST.get("qty")
                charged_weight = request.POST.get("charged_weight")
                actual_weight = request.POST.get("actual_weight")
                declare_value = request.POST.get("declare_value")
                freight_charge = request.POST.get("freight_charge")
                pod_charge = request.POST.get("pod_charge")
                spcl_del_charge = request.POST.get("spcl_del_charge")
                insurance_amount = request.POST.get("insurance_amount")
                insurance_percentage = request.POST.get("insurance_percentage")
                gst_rate = request.POST.get("gst_rate")
                gst_rate = GstModel.objects.get(id=gst_rate)
                gst_amount = request.POST.get("gst_amount")
                gst_amount = float(gst_amount)
                gst_radio = request.POST.get("cs_i_gst")
                mode_amount = request.POST.get("mode_amount")
                booking_mode = request.POST.get("booking_mode")

                if gst_radio == "true":
                    gst_radio = True
                else:
                    gst_radio = False
                total_amount = request.POST.get("total_amount")            
                party_name = PartyAccounts.objects.get(party_name__icontains="cash", user=request.user)                
                remarks = request.POST.get("remarks")            
                if not update_id:            
                    if not existing_c_note:       
                        request.session["next_c_note_for_cash"] = ""                     
                        booking_obj = Booking.objects.create(c_note_number=c_note_number, party_name=party_name, 
                                        booking_type=booking_type, doc_date=booking_datetime,
                                        payment_mode=payment_mode, ref_courier_name=ref_courier_name, ref_courier_number=ref_number,
                                        sender_name=sender_name, sender_mobile=sender_mobile, sender_address=sender_address,
                                        from_destination=from_destination, gst_number=gst_number, e_way_bill_number=e_way_bill, receiver_name=receiver_name,
                                        receiver_mobile_number=receiver_mobile, receiver_address=receiver_address, to_destination=to_destination,
                                        pincode=pincode, state=state, pcs=qty, charged_weight=charged_weight, weight=actual_weight,
                                        declared_value=declare_value, freight_charge=freight_charge, pod_charge=pod_charge, spl_del_charge=spcl_del_charge,
                                        insurance_amt=insurance_amount, insurance_per=insurance_percentage, gst_rate=gst_rate, gst_amount=gst_amount,
                                        c_i_gst=gst_radio, amount=total_amount, remarks=remarks, mode_amount=mode_amount, booking_mode=booking_mode,
                                        user=request.user)                    
                        booking_obj.save()                    
                        request.session["success"] = "success"
                        try:
                            request.session["next_c_note_for_cash"] = int(c_note_number) + 1
                        except:
                            pass
                        messages.success(request, "Shipment booked Successfully.")
                        return JsonResponse({"status": 1, "message": "Shipment booked Successfully", "print_id": booking_obj.id})                       
                    else:                    
                        return JsonResponse({"status": 0, "message": "C Note Already exists"})         
                else:                                                                   
                    booking_obj = Booking.objects.get(id=update_id)            
                    booking_obj.c_note_number=c_note_number
                    booking_obj.party_name=party_name
                    booking_obj.booking_type=booking_type 
                    booking_obj.doc_date=booking_datetime                                    
                    booking_obj.payment_mode=payment_mode 
                    booking_obj.ref_courier_name=ref_courier_name 
                    booking_obj.ref_courier_number=ref_number
                    booking_obj.sender_name=sender_name
                    booking_obj.sender_mobile=sender_mobile 
                    booking_obj.sender_address=sender_address
                    booking_obj.from_destination=from_destination 
                    booking_obj.gst_number=gst_number
                    booking_obj.e_way_bill_number=e_way_bill 
                    booking_obj.receiver_name=receiver_name
                    booking_obj.receiver_mobile_number=receiver_mobile 
                    booking_obj.receiver_address=receiver_address
                    booking_obj.to_destination=to_destination
                    booking_obj.pincode=pincode
                    booking_obj.state=state 
                    booking_obj.pcs=qty
                    booking_obj.charged_weight=charged_weight 
                    booking_obj.weight=actual_weight
                    booking_obj.declared_value=declare_value 
                    booking_obj.freight_charge=freight_charge 
                    booking_obj.pod_charge=pod_charge
                    booking_obj.spl_del_charge=spcl_del_charge
                    booking_obj.insurance_amt=insurance_amount 
                    booking_obj.insurance_per=insurance_percentage 
                    booking_obj.gst_rate=gst_rate
                    booking_obj.gst_amount=gst_amount
                    booking_obj.c_i_gst=gst_radio
                    booking_obj.amount=total_amount 
                    booking_obj.remarks=remarks
                    booking_obj.mode_amount = mode_amount
                    booking_obj.booking_mode = booking_mode
                    booking_obj.user=request.user                
                    booking_obj.save()            
                    request.session["success"] = "success"
                    messages.success(request, "Shipment updated Successfully.")
                    return JsonResponse({"status": 1, "message": "Shipment updated Successfully"})                       
            else:            
                return JsonResponse({"status": 0, "message": "Invalid C. Note number"})
        except Exception as e:
            log.exception(e)
            return JsonResponse({"status": 0, "message": "Internal server error, kindly contact with admin."})
    return JsonResponse({"status": 0, "message": "Get method not allowed."})

@login_required(login_url="login_auth")
def check_c_note_num(request):
    try:
        if request.method == "POST":
            c_note_number = int(request.POST.get("c_note_number", 1))               
            process_further = False
            c_note_details = CNoteGenerator.objects.filter(user=request.user)
            for i in c_note_details:            
                if int(i.from_range) <= int(c_note_number) <= int(i.to_range):
                    process_further = True 
                    break                                        
            if process_further:
                booking_obj = Booking.objects.filter(c_note_number=c_note_number, user=request.user)
                if not booking_obj.exists():
                    return JsonResponse({"status": 1})
            return JsonResponse({"status": 0, "message": "Insert correct C. Note number !"})
        return JsonResponse({"status": 0, "message": "Get method not allowed."})
    except Exception as e:
        log.exception(e)
        return JsonResponse({"status": 0, "message": "Insert correct docket number."})


@login_required(login_url="login_auth")
def edit_cash_booking(request, booking_num):
    try:
        booking_num = int(booking_num)
        booking_details = Booking.objects.get(id=booking_num, user=request.user)
        booking_type = BookingType.objects.all()
        ref_courier_name = RefCourier.objects.all()
        from_destination = UserAdditionalDetails.objects.get(user=request.user)             
        states = State.objects.all()
        gst_rates = GstModel.objects.all()        
        context = {"ref_courier_names": ref_courier_name,               
                "booking_type": booking_type,                
                "from_destination": from_destination,
                "states": states, "gst_rates": gst_rates, 
                "edit_page": 1, "booking_details": booking_details} 
        return render(request, "cash_booking.html", context=context)
    except:
        return redirect("booking_dashboard")        

@login_required(login_url="login_auth")
def print_cash_booking(request, sid):       
    try:
        booking_details = Booking.objects.get(user=request.user, id=sid)
        user_details = BranchNetwork.objects.get(user=request.user)
        c_number = str(booking_details.c_note_number)
        # Generate barcde
        barcode_svg = BARCODE_CLASS(c_number).render(writer_options={"module_width": float(.29),
                                                "module_height": float(10)}).decode("utf8")   
        # Generate QR Code        
        qr_url = (f"https://airpostxpress.com/tracking/{str(c_number)}")
        qr_code = pyqrcode.create(qr_url)                
        svg_buffer = io.BytesIO()
        qr_code.svg(svg_buffer, scale=10, module_color='#000', background='#fff')
        svg_buffer.seek(0)        
        svg_base64 = base64.b64encode(svg_buffer.getvalue()).decode()        
        qr_code = f'<img src="data:image/svg+xml;base64,{svg_base64}" width="90" height="90" alt="QR Code">'
        context = {"bd": booking_details, "ud": user_details, "barcode": barcode_svg, "qr_code": qr_code}
        
        
        return render(request, "print_cash_booking.html", context=context)    
    except Exception as e:
        log.exception(e)
    
    return redirect("booking_dashboard")


@login_required(login_url="login_auth")
def advance_date_wise_search_cash_booking(request):
    try:
        if request.method == "POST":
            from_date = request.POST.get("from_date")        
            to_date = request.POST.get("to_date")
            from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
            to_date = to_date + timedelta(days=1)        
            data = Booking.objects.filter(doc_date__range=(from_date, to_date), 
                    user=request.user).order_by("-created_at").values("id",
                        "c_note_number", "doc_date", "to_destination__name", "booking_type__booking_type",
                        "party_name__party_name", "receiver_name", "weight", "freight_charge", "amount", 
                        "ref_courier_name__name", "booking_mode")        
            return JsonResponse({"status": 1, "data": list(data)})

        else:            
            return JsonResponse({"status": 0})
    except Exception as e:
        log.exception(e)
        return JsonResponse({"status": 0})

@login_required(login_url="login_auth")
def advance_date_party_wise_search_cash_booking(request):
    try:
        if request.method == "POST":
            from_date = request.POST.get("from_date")        
            to_date = request.POST.get("to_date")        
            party = request.POST.get("party")
            party = PartyAccounts.objects.get(id=party)
            from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
            to_date = to_date + timedelta(days=1)        
            data = Booking.objects.filter(doc_date__range=(from_date, to_date), user=request.user, party_name=party).order_by("-created_at").values("id", "c_note_number", "doc_date", "to_destination__name", "booking_type__booking_type", "party_name__party_name", "receiver_name", "weight", "freight_charge", "amount", "ref_courier_name__name", "booking_mode")        
            return JsonResponse({"status": 1, "data": list(data)})
        else:
            return JsonResponse({"status": 0})
    except Exception as e:
        log.exception(e)
        return JsonResponse({"status": 0})

@login_required(login_url="login_auth")
def advance_c_note_wise_search_cash_booking(request):
    try:
        if request.method == "POST":                      
            c_note = request.POST.get("c_note")            
            try:                             
                c_note = int(c_note)                                           
            except:                                
                if not c_note:
                    today_date = datetime.date.today()                                    
                    data = Booking.objects.filter(created_at__startswith=today_date, user=request.user).order_by("-created_at").values("id", "c_note_number", "doc_date", "to_destination__name", "booking_type__booking_type", "party_name__party_name", "receiver_name", "weight", "freight_charge", "amount", "ref_courier_name__name", "booking_mode")        
                    
                    return JsonResponse({"status": 1, "data": list(data)})
            data = Booking.objects.filter(user=request.user, c_note_number=c_note).order_by("-created_at").values("id", "c_note_number", "doc_date", "to_destination__name", "booking_type__booking_type", "party_name__party_name", "receiver_name", "weight", "freight_charge", "amount", "ref_courier_name__name", "booking_mode")        
            return JsonResponse({"status": 1, "data": list(data)})
        else:
            return JsonResponse({"status": 0})
    except Exception as e:
        log.exception(e)
        return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def advance_date_ref_courier_wise_search_cash_booking(request):
    try:
        if request.method == "POST":
            from_date = request.POST.get("from_date")        
            to_date = request.POST.get("to_date")        
            ref_courier = request.POST.get("ref_courier")
            ref_courier = RefCourier.objects.get(id=ref_courier)
            from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
            to_date = to_date + timedelta(days=1)        
            data = Booking.objects.filter(doc_date__range=(from_date, to_date), user=request.user, ref_courier_name=ref_courier).order_by("-created_at").values("id", "c_note_number", "doc_date", "to_destination__name", "booking_type__booking_type", "party_name__party_name", "receiver_name", "weight", "freight_charge", "amount", "ref_courier_name__name", "booking_mode")        
            return JsonResponse({"status": 1, "data": list(data)})
        else:
            return JsonResponse({"status": 0})
    except Exception as e:
        return JsonResponse({"status": 0})

# ########################################## Fast Booking details  ###########################

@login_required(login_url="login_auth")
def bookings(request):    
    # destinations = Destination.objects.all()    
    ref_courier_name = RefCourier.objects.all()    
    booking_type = BookingType.objects.all().order_by("-booking_type")
    parties = PartyAccounts.objects.filter(user=request.user).order_by("party_name")
    today_date = datetime.date.today()    
    today_bookings = {} # Booking.objects.filter(created_at__startswith=today_date, user=request.user, booking_mode="A/C").order_by("-created_at")    
    from_destination = UserAdditionalDetails.objects.get(user=request.user)        
    context = {"ref_courier_name": ref_courier_name,
               "parties": parties, "today_bookings": today_bookings,
               "booking_type": booking_type,
               "total_bookings": len(today_bookings), 
               "from_destination": from_destination}                
    return render(request, "bookings.html", context=context)


@login_required(login_url="login_auth")
def account_booking_return(request):
    if request.method == "POST":
        today_date = datetime.date.today()  
        from_date = request.session.get("f_b_from_date", None)
        to_date = request.session.get("f_b_to_date", None)        
        if from_date and to_date:   # To return data of existing searched dates.
            try:
                from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
                to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
                to_date = to_date + timedelta(days=1)        
                today_bookings = Booking.objects.filter(doc_date__range=(from_date, to_date),
                        user=request.user, booking_mode="A/C").order_by("-created_at").values("id", "c_note_number", "to_destination__name", 
                                        "ref_courier_name__name", "doc_date", "booking_type__booking_type",
                                        "party_name__party_name", "weight")  
                return JsonResponse({"status": 1, "data": list(today_bookings)})
            except Exception as e:
                log.error("Fast booking search dates are set to blank thats why below error occur.")
                log.exception(e)
        today_bookings = Booking.objects.filter(created_at__startswith=today_date,
                user=request.user, booking_mode="A/C").order_by("-created_at").values("id", "c_note_number", "to_destination__name", 
                                "ref_courier_name__name", "doc_date", "booking_type__booking_type",
                                "party_name__party_name", "weight")  
                        
        return JsonResponse({"status": 1, "data": list(today_bookings)})
    return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def save_booking(request):
    try:
        if request.method == "POST":        
            c_note_number = request.POST.get("cnotenumber")
            request.session["success"] = None
            process_further = False
            c_note_details = CNoteGenerator.objects.filter(user=request.user)
            for i in c_note_details:            
                if int(i.from_range) <= int(c_note_number) <= int(i.to_range):
                    process_further = True 
                    break                            
            
            if process_further:
                update_id = request.POST.get("id")                              
                existing_c_note = Booking.objects.filter(c_note_number=c_note_number)                        
                party_name = request.POST.get("party")              
                request.session["party_name"] = party_name
                party_name = PartyAccounts.objects.get(id=party_name)    
                booking_type = request.POST.get("bookingtype")  
                request.session["booking_type"] = booking_type
                booking_type = BookingType.objects.get(id=booking_type)
                booking_datetime = request.POST.get("datetime")        
                from_dest = request.POST.get("from_destination")
                request.session["from_dest"] = from_dest
                from_dest = Destination.objects.get(id=from_dest)
                to_dest = request.POST.get("todest")
                request.session["to_dest"] = to_dest
                to_dest = Destination.objects.get(id=to_dest)
                s_name = request.POST.get("s_name")
                request.session["p_sender_name"] = s_name
                s_number = request.POST.get("s_number")
                r_name = request.POST.get("r_name")
                r_number = request.POST.get("r_number")        
                ref_courier = request.POST.get("ref_courier")        
                ref_courier = RefCourier.objects.get(id=ref_courier)
                ref_number = request.POST.get("ref_number")
                remarks = request.POST.get("remarks")
                amount = request.POST.get("amount")
                weight = request.POST.get("weight") 
                qty = request.POST.get("qty")           
                if not update_id:            
                    if not existing_c_note:        
                        request.session["next_c_note"] = ""                    
                        booking_obj = Booking.objects.create(doc_date=booking_datetime, party_name=party_name,
                        c_note_number=c_note_number, from_destination=from_dest, to_destination=to_dest, booking_type=booking_type,
                        sender_name=s_name, sender_mobile=s_number, receiver_name=r_name, receiver_mobile_number=r_number,
                        ref_courier_name=ref_courier, ref_courier_number=ref_number, user=request.user, remarks=remarks, 
                        amount=amount, weight=weight, charged_weight=weight, freight_charge=amount, pcs=qty, booking_mode="A/C")                    
                        booking_obj.save()                          
                        request.session["success"] = "success"
                        request.session["f_b_from_date"] = None
                        request.session["f_b_to_date"] = None
                        try:
                            request.session["next_c_note"] = int(c_note_number) + 1
                        except:
                            pass
                        messages.success(request, "Shipment booked Successfully.")
                        return redirect("bookings")
                    else:
                        messages.error(request, 'C Note Already exists')            
                else:            
                    booking_obj = Booking.objects.get(id=update_id)            
                    booking_obj.doc_date = booking_datetime
                    booking_obj.party_name = party_name
                    booking_obj.booking_type = booking_type
                    booking_obj.c_note_number = c_note_number
                    booking_obj.from_destination = from_dest
                    booking_obj.to_destination = to_dest
                    booking_obj.sender_name = s_name
                    booking_obj.sender_mobile = s_number
                    booking_obj.receiver_name = r_name
                    booking_obj.receiver_mobile_number = r_number
                    booking_obj.ref_courier_name = ref_courier
                    booking_obj.ref_courier_number = ref_number 
                    booking_obj.remarks = remarks
                    booking_obj.amount = amount
                    booking_obj.weight = weight
                    booking_obj.charged_weight = weight
                    booking_obj.freight_charge = amount
                    booking_obj.pcs=qty
                    booking_obj.user=request.user  
                    booking_obj.booking_mode = "A/C"                  
                    booking_obj.save()            
                    request.session["success"] = "success"
                    messages.success(request, "Shipment updated Successfully.")
                    return redirect("bookings")                       
            else:
                messages.success(request, "Invalid C. Note number")
    except Exception as e:
        log.error(f"Fast booking error for user {request.user}")
        log.exception(e)    
    return redirect("bookings")

@login_required(login_url="login_auth")
def edit_data_retrive(request):
    try:
        if request.method == "POST":
            id = request.POST.get("id")        
            data = Booking.objects.filter(pk=id).values("id", "doc_date", "party_name", "c_note_number", 
            "from_destination", "to_destination", "sender_name", "sender_mobile", "receiver_name", "receiver_mobile_number",
            "ref_courier_name", "ref_courier_number", "booking_type", "amount", "remarks", "weight", "pcs")                      
            return JsonResponse({"data": list(data)})
    except Exception as e:
        log.exception(e)
    return JsonResponse({"status": 0, "data": []})

@login_required(login_url="login_auth")
def advance_search_by_date(request):
    try:
        if request.method == "POST":
            from_date =  request.POST.get("from_date")
            to_date =  request.POST.get("to_date")
            request.session["f_b_from_date"] = from_date
            request.session["f_b_to_date"] = to_date      
            from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
            to_date = to_date + timedelta(days=1)        
            data = Booking.objects.filter(doc_date__range=(from_date, to_date), user=request.user,
                     booking_mode="A/C").values("id", "c_note_number", "to_destination__name", 
                                "ref_courier_name__name", "doc_date", "booking_type__booking_type",
                                "party_name__party_name", "weight")        
            if data:            
                return JsonResponse({"status": 1, "data": list(data)})
            else:
                return JsonResponse({"ststua": 0})
        else:
            return JsonResponse({"ststua": 0})
    except Exception as e:
        return JsonResponse({"ststua": 0})

@login_required(login_url="login_auth")
def advance_search_by_c_note(request):
    try:
        if request.method == "POST":
            c_note_number =  request.POST.get("c_note_number")                
            data = Booking.objects.filter(c_note_number=c_note_number, user=request.user, 
                        booking_mode="A/C").values("id", "c_note_number", 
                        "to_destination__name", "ref_courier_name__name", "doc_date", "booking_type__booking_type",
                                "party_name__party_name", "weight")
            if data:            
                return JsonResponse({"status": 1, "data": list(data)})
            else:
                return JsonResponse({"ststua": 0})
        else:
            return JsonResponse({"ststua": 0})
    except Exception as e:
        log.exception(e)
    return JsonResponse({"ststua": 0})

@login_required(login_url="login_auth")
def advance_search_for_ref_number(request):
    if request.method == "POST":
        ref_number =  request.POST.get("ref_number")                
        data = Booking.objects.filter(ref_courier_number=ref_number, user=request.user,
                    booking_mode="A/C").values("id", "c_note_number", "to_destination__name",
                "ref_courier_name__name", "doc_date", "booking_type__booking_type",
                                "party_name__party_name", "weight")
        if data:            
            return JsonResponse({"status": 1, "data": list(data)})
        else:
            return JsonResponse({"ststua": 0})
    else:
        return JsonResponse({"ststua": 0})


# ############################# Party Details start ###################################################

@login_required(login_url="login_auth")
def part_master(request):
    parties = PartyAccounts.objects.filter(user=request.user).order_by("party_name")
    total_parties = len(parties)
    context = {"parties": parties, "total_parties": total_parties}
    return render(request, "party_master.html", context)


@login_required(login_url="login_auth")
def save_parties(request):
    if request.method == "POST":
        id_of = request.POST.get("id")
        party_name = request.POST.get("party_name")
        mobile_number = request.POST.get("mobile_number")
        password = request.POST.get("password")
        opening_balance = request.POST.get("opening_balance")
        request.session["success"] = None
        if id_of:
            party = PartyAccounts(id=id_of, party_name=party_name, mobile_number=mobile_number, user=request.user, 
            opening_balance=opening_balance, password=password)
            party.save()
            messages.success(request, "Party Details updated succsessfully.")
            request.session["success"] = "success"
        else:
            available_party = PartyAccounts.objects.filter(mobile_number=mobile_number)
            if available_party:
                messages.error(request, "Party number already exists.")
            else:
                party = PartyAccounts(party_name=party_name, mobile_number=mobile_number, user=request.user, 
                opening_balance=opening_balance, password=password)
                party.save()
                messages.success(request, "Party Details added succsessfully.")
                request.session["success"] = "success"

        # parties = PartyAccounts.objects.filter(user=request.user)
        # total_parties = len(parties)
        # context = {"parties": parties, "total_parties": total_parties}  

        return redirect("part_master")

    else:
        return redirect("part_master")

@login_required(login_url="login_auth")
def edit_party_details(request):
    if request.method == "POST":
        id = request.POST.get("id")        
        try:
            data = PartyAccounts.objects.get(id=id)
            data = {"id": data.id, "party_name": data.party_name, "mobile_number": data.mobile_number, "password": data.password,
             "opening_balance": data.opening_balance}
            return JsonResponse({"status": 1, "data": data})
        except Exception as e:
            log.exception(e)
            return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def delete_party_detail(request):
    id_of = request.POST.get("id")
    try:
        data = PartyAccounts.objects.get(id=id_of)
        data.delete()        
        data = PartyAccounts.objects.filter(user=request.user).values()      
        total_parties = len(data)        
        return JsonResponse({"status": 1, "data": list(data), "total_parties": total_parties})

    except Exception as e:
        log.exception(e)


# ############################## TRACKING HISTORY IN start ##########################################

@login_required(login_url="login_auth")
def tracking_history_in(request):
    # destinations = Destination.objects.all()
    today_date = datetime.date.today()    
    status = ParcelStatus.objects.get(name="IN")  
    today_in = Trackinghistory.objects.filter(user=request.user, last_updated_datetime__startswith=today_date, status=status).order_by("-last_updated_datetime")
    context = {"doc_in": today_in}    
    return render(request, "tracking_history.html", context=context)


@login_required(login_url="login_auth")
def save_input_load(request):
    if request.method == "POST":
        id_of = request.POST.get("id_of")                
        date = request.POST.get("date")
        from_destination = request.POST.get("from_destination")        
        c_note_number = request.POST.get("c_note_number")
        remarks = request.POST.get("remarks")
        try:
            c_note_number_booking = Booking.objects.get(c_note_number=c_note_number)                 
            user = request.user
            try:
                status = ParcelStatus.objects.get(name="IN")        
                try:
                    to_destination = UserAdditionalDetails.objects.get(user=request.user)                
                    to_destination = to_destination.destination
                    try:                        
                        # from_destination = Destination.objects.get(id=from_destination)  
                        old_chain_details = Trackinghistory.objects.filter(c_note_number=c_note_number_booking).order_by("-in_out_datetime")
                        if old_chain_details.exists():                            
                            from_destination = Destination.objects.get(id=old_chain_details[0].d_from.id)
                        else:
                            from_destination = Destination.objects.get(id=c_note_number_booking.from_destination.id)                        
                        if id_of:
                            saved_data = Trackinghistory.objects.get(id=id_of)
                            saved_data.c_note_number = c_note_number_booking
                            saved_data.remarks = remarks
                            saved_data.d_from = from_destination
                            saved_data.in_out_datetime = date
                            saved_data.save()                                               
                        else:            
                            today_date = str(date)[:10]                            
                            if_available = Trackinghistory.objects.filter(user=request.user, in_out_datetime__startswith=today_date, status=status, c_note_number=c_note_number_booking)                            
                            if if_available:
                                return JsonResponse({"status": 0, "message": "Duplicate entry found."}) 
                            Trackinghistory.objects.create(c_note_number=c_note_number_booking, in_out_datetime=date,
                                    d_from=from_destination, d_to=to_destination, status=status, remarks=remarks, user=user)                                                
                        # data = Trackinghistory.objects.values()
                        today_date = datetime.date.today()      
                        today_in = Trackinghistory.objects.filter(user=request.user, last_updated_datetime__startswith=today_date, status=status).order_by("-last_updated_datetime")
                        today_in = list(today_in.values("id", "c_note_number__c_note_number", "d_from__name", "remarks"))
                        return JsonResponse({"status": 1, "data": today_in})
                    except Exception as e:                        
                        return JsonResponse({"status": 0, "message": "From destination Not found."}) 
                except Exception as e:                    
                    return JsonResponse({"status": 0, "message": "User destination Not found."}) 
            except:
                return JsonResponse({"status": 0, "message": "Status Not found."})                    
        except:            
            return JsonResponse({"status": 0, "message": "C Note Number Not found."})


    return JsonResponse({"status": 0})

@login_required(login_url="login_auth")
def load_in_delete(request):
    if request.method == "POST":
        id_of = request.POST.get("id_of")
        data = Trackinghistory.objects.get(id=id_of)
        data.delete()        
        return JsonResponse({"status": 1})
    else:
        return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def load_in_edit(request):
    if request.method == "POST":        
        id_of = request.POST.get("id_of")
        data = Trackinghistory.objects.filter(id=id_of).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_from", "remarks", "d_to")                            
        return JsonResponse({"status": 1, "data": list(data)})       


@login_required(login_url="login_auth")
def advance_search_by_c_note_load_in(request):
    if request.method == "POST":
        c_note_number = request.POST.get("c_note_number")
        try:
            status = ParcelStatus.objects.get(name="IN")            
            c_note_number = Booking.objects.get(c_note_number=c_note_number)   
            data = Trackinghistory.objects.filter(user=request.user, c_note_number=c_note_number, status=status).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_from__name", "remarks")        
            return JsonResponse({"status": 1, "data": list(data)})    
        except:
            return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def advance_search_by_ref_num_load_in(request):
    if request.method == "POST":
        ref_number = request.POST.get("ref_number")
        try:
            status = ParcelStatus.objects.get(name="IN")            
            ref_number = Booking.objects.get(ref_courier_number=ref_number)   
            data = Trackinghistory.objects.filter(user=request.user, c_note_number=ref_number, status=status).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_from__name", "remarks")                    
            return JsonResponse({"status": 1, "data": list(data)})    
        except:
            return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def advance_search_load_in_by_date(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
        to_date = to_date + timedelta(days=1)
        status = ParcelStatus.objects.get(name="IN")        
        data = Trackinghistory.objects.filter(in_out_datetime__range=(from_date, to_date), user=request.user,
                                              status=status).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_from__name", "remarks")        
        return JsonResponse({"status": 1, "data": list(data)})
    else:
        return JsonResponse({"status": 0})

# ##################################### Tracking history OUT start #######################################

@login_required(login_url="login_auth")
def tracking_history_out(request):
    # destinations = Destination.objects.all()
    today_date = datetime.date.today()    
    status = ParcelStatus.objects.get(name="OUT")
    today_in = Trackinghistory.objects.filter(user=request.user, last_updated_datetime__startswith=today_date, status=status).order_by("-last_updated_datetime")
    context = {"doc_in": today_in}    
    return render(request, "tracking_history_out.html", context=context)


@login_required(login_url="login_auth")
def save_output_load(request):
    if request.method == "POST":
        id_of = request.POST.get("id_of")                
        date = request.POST.get("date")
        new_dt = str(date)[:10]  
        from_destination = request.POST.get("from_destination")        
        c_note_number = request.POST.get("c_note_number")
        remarks = request.POST.get("remarks")
        try:
            c_note_number_booking = Booking.objects.get(c_note_number=c_note_number)                 
            user = request.user
            try:
                status = ParcelStatus.objects.get(name="OUT")        
                try:
                    to_destination = UserAdditionalDetails.objects.get(user=request.user)                
                    to_destination = to_destination.destination
                    try:                        
                        from_destination = Destination.objects.get(id=from_destination)                                                
                        if id_of:
                            saved_data = Trackinghistory.objects.get(id=id_of)
                            saved_data.c_note_number = c_note_number_booking
                            saved_data.remarks = remarks
                            saved_data.d_to = from_destination
                            saved_data.in_out_datetime = date
                            saved_data.save()                                               
                        else:
                            if_available = Trackinghistory.objects.filter(c_note_number=c_note_number_booking, 
                            in_out_datetime__startswith=new_dt, user=request.user, status=status)                            
                            if if_available:
                                return JsonResponse({"status": 0, "message": "Duplicate entry found."})                         
                            Trackinghistory.objects.create(c_note_number=c_note_number_booking, in_out_datetime=date,
                                    d_from=to_destination, d_to=from_destination, status=status, remarks=remarks, user=user)                                                
                        # data = Trackinghistory.objects.values()
                        # today_date = datetime.date.today()            
                        # date = str(date)[:10]                                   
                        today_in = Trackinghistory.objects.filter(user=request.user, in_out_datetime__startswith=new_dt, status=status, d_to=from_destination).order_by("-last_updated_datetime")
                        today_in = list(today_in.values("id", "c_note_number__c_note_number", "d_to__name", "remarks"))
                        return JsonResponse({"status": 1, "data": today_in})
                    except Exception as e:                        
                        return JsonResponse({"status": 0, "message": "From destination Not found."}) 
                except Exception as e:                    
                    return JsonResponse({"status": 0, "message": "User destination Not found."}) 
            except:
                return JsonResponse({"status": 0, "message": "Status Not found."})            
        
        except:            
            return JsonResponse({"status": 0, "message": "C Note Number Not found."})

    return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def advance_search_by_c_note_load_out(request):
    if request.method == "POST":
        c_note_number = request.POST.get("c_note_number")
        try:
            status = ParcelStatus.objects.get(name="OUT")            
            c_note_number = Booking.objects.get(c_note_number=c_note_number)   
            data = Trackinghistory.objects.filter(user=request.user, c_note_number=c_note_number, status=status).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_to__name", "remarks")        
            return JsonResponse({"status": 1, "data": list(data)})    
        except:
            return JsonResponse({"status": 0})

@login_required(login_url="login_auth")
def advance_search_by_ref_num_load_out(request):
    if request.method == "POST":
        ref_number = request.POST.get("ref_number")
        try:
            status = ParcelStatus.objects.get(name="OUT")            
            ref_number = Booking.objects.get(ref_courier_number=ref_number)   
            data = Trackinghistory.objects.filter(user=request.user, c_note_number=ref_number, status=status).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_to__name", "remarks")                    
            return JsonResponse({"status": 1, "data": list(data)})    
        except:
            return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def advance_search_load_out_by_date(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
        to_date = to_date + timedelta(days=1)
        status = ParcelStatus.objects.get(name="OUT")        
        data = Trackinghistory.objects.filter(in_out_datetime__range=(from_date, to_date), user=request.user,
                                              status=status).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_to__name", "remarks")        
        return JsonResponse({"status": 1, "data": list(data)})
    else:
        return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def load_out_auto_search_by_date_and_des(request):
    if request.method == "POST":
        date = request.POST.get("date")[:10]
        to_destination = request.POST.get("destination")         
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()        
        to_date = date + timedelta(days=1)
        destination = Destination.objects.get(id=to_destination)
        status = ParcelStatus.objects.get(name="OUT")        
        data = Trackinghistory.objects.filter(in_out_datetime__range=(date, to_date), user=request.user,
                                              d_to=destination, status=status).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_to__name", "remarks")        
        return JsonResponse({"status": 1, "data": list(data)})
    else:
        return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def load_out_auto_search_by_date_auto(request):
    if request.method == "POST":
        date = request.POST.get("date")[:10]             
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()        
        to_date = date + timedelta(days=1)        
        status = ParcelStatus.objects.get(name="OUT")        
        data = Trackinghistory.objects.filter(in_out_datetime__range=(date, to_date), user=request.user,
                                              status=status).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_to__name", "remarks")        
        return JsonResponse({"status": 1, "data": list(data)})
    else:
        return JsonResponse({"status": 0})


# ####################### Area master start here ########################### 

@login_required(login_url="login_auth")
def area_master(request):
    areas = AreaMaster.objects.filter(user=request.user)
    pincodes = BranchNetwork.objects.all()
    total_areas = len(areas)
    context = {"areas": areas, "total_areas": total_areas, "pincodes": pincodes}
    return render(request, "area_master.html", context)    


@login_required(login_url="login_auth")
def save_area_master(request):    
    if request.method == "POST":
        id_of = request.POST.get("id")
        area_name = request.POST.get("area_name")
        pincode = request.POST.get("pincode")        
        pincode = BranchNetwork.objects.get(id=pincode)                
        request.session["success"] = None
        if not id_of:
            area_master = AreaMaster(area_name=area_name, pincode=pincode, user=request.user)
            area_master.save()
            messages.success(request, "Area Details added succsessfully.")
            request.session["success"] = "success"
        else:
            area_master = AreaMaster(id=id_of, area_name=area_name, pincode=pincode, user=request.user)
            area_master.save()
            messages.success(request, "Area Details updated succsessfully.")
            request.session["success"] = "success"            

    return redirect("area_master")


@login_required(login_url="login_auth")
def edit_area_details(request):    
    if request.method == "POST":  
        try:      
            id_of = request.POST.get("id")
            area_details = AreaMaster.objects.get(id=id_of)        
            data = {"id": area_details.id, "area_name": area_details.area_name, "pincode": area_details.pincode.id}                        
            return JsonResponse({"status": 1, "data": data})
        except Exception as e:
            log.exception(e)  

    return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def delete_area_detail(request):
    if request.method == "POST":
        try:
            id_of = request.POST.get("id")
            area_details = AreaMaster.objects.get(id=id_of)
            area_details.delete()
            area_details = AreaMaster.objects.filter(user=request.user).values("id", "area_name", "pincode__pincode")               
            total_areas = len(area_details)        

            return JsonResponse({"status": 1, "data": list(area_details), "total_areas": total_areas})
        except Exception as e:
            log.exception(e)  
        
        return JsonResponse({"status": 0})

# ########################################### Delivery Area Master ###############################
@login_required(login_url="login_auth")
def delivery_area_master(request):
    data = Network.objects.filter(user=request.user).order_by("pincode")
    return render(request, "delivery_area_master.html", context={"data": data})

@login_required(login_url="login_auth")
def save_delivery_area_master_details(request):
    if request.method == "POST":
        try:            
            pincode = int(request.POST.get("pincode"))
            delivery_areas = request.POST.get("delivery_areas")
            non_del_areas = request.POST.get("non_delivery_areas")
            chargeable_del_areas = request.POST.get("chargeable_delivery_areas")
            saved_details = Network.objects.filter(user=request.user, pincode=pincode)                                    
            if not saved_details.exists():                            
                Network(pincode=pincode, delivery_areas=delivery_areas, non_delivery_area=non_del_areas, 
                        chargeable_delivery_area=chargeable_del_areas, user=request.user).save()
                messages.success(request, "Delivery areas added successfully.")
            else:  
                old_details = Network.objects.get(user=request.user, pincode=pincode)
                old_details.delivery_areas = delivery_areas
                old_details.non_delivery_area=non_del_areas
                old_details.chargeable_delivery_area=chargeable_del_areas
                old_details.save()
                messages.success(request, "Delivery areas updated successfully.")                
        except Exception as e:
            log.exception(e)

    return redirect("delivery_area_master")

@login_required(login_url="login_auth")
def delete_del_area_master(request):
    if request.method == "POST":
        try:
            id_of = request.POST.get("id_of")
            Network.objects.get(id=id_of).delete() 
            messages.success(request, "Pincode details deleted successfully.")   
            return JsonResponse({"status": 1})
        except Exception as e:            
            log.exception(e)            
    return JsonResponse({"status": 0})

@login_required(login_url="login_auth")
def edit_del_area_master(request):
    if request.method == "POST":
        try:
            id_of = request.POST.get("id_of")
            details = Network.objects.get(id=id_of, user=request.user)            
            details = {"pincode": details.pincode, "delivery_areas": details.delivery_areas, 
                       "non_del_areas": details.non_delivery_area, "ch_del_areas": details.chargeable_delivery_area }            
            return JsonResponse({"status": 1, "data": details})
        except Exception as e:
            log.exception(e)

    return JsonResponse({"status": 0})

# ########################################### Delivery boy master ################################

@login_required(login_url="login_auth")
def delivery_boy_master(request):
    area_details = AreaMaster.objects.filter(user=request.user).values("id", "area_name", "pincode__pincode")        
    delivery_boys = DeliveryBoyMaster.objects.filter(user=request.user).values("id", "delivery_boy_name", "mobile_number", "area_name__area_name")    
    total_boys = len(delivery_boys)
    context={"area_details": area_details, "total_boys": total_boys, "delivery_boys": delivery_boys}
    return render(request, "delivery_boy_master.html", context)

@login_required(login_url="login_auth")
def save_delivery_boy_details(request):
    if request.method == "POST":
        id_of = request.POST.get("id")
        delivery_boy_name = request.POST.get("delivery_boy_name")
        mobile_number = request.POST.get("mobile_number")
        alternate_number = request.POST.get("alternate_number")
        email = request.POST.get("email")
        area = request.POST.get("area")
        area = AreaMaster.objects.get(id=area)
        request.session["success"] = None
        if not id_of:
            delivery_boy = DeliveryBoyMaster(delivery_boy_name=delivery_boy_name, mobile_number=mobile_number,
                                             alternate_number=alternate_number, email=email, area_name=area, user=request.user)
            delivery_boy.save()
            messages.success(request, "Delivery boy added succsessfully.")
            request.session["success"] = "success"
        else:
            delivery_boy = DeliveryBoyMaster(id=id_of, delivery_boy_name=delivery_boy_name, mobile_number=mobile_number,
                                             alternate_number=alternate_number, email=email, area_name=area, user=request.user)
            delivery_boy.save()
            messages.success(request, "Delivery boy updated succsessfully.")
            request.session["success"] = "success"        

    return redirect("delivery_boy_master")


@login_required(login_url="login_auth")
def edit_delivery_boy_details(request):
    if request.method == "POST":
        try:
            id_of = request.POST.get("id")            
            data = DeliveryBoyMaster.objects.get(id=id_of)
            data = {"id": data.id, "delivery_boy_name": data.delivery_boy_name, "mobile_number": data.mobile_number,
                    "alternate_number": data.alternate_number, "email": data.email, "area_name": data.area_name.area_name, "area_id": data.area_name.id}                                    
            return JsonResponse({"status": 1, "data": data})
        except Exception as e:
            log.exception(e)  
    return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def delete_delivery_boy_detail(request):
    if request.method == "POST":
        try:
            id_of = request.POST.get("id")
            delivery_boy = DeliveryBoyMaster.objects.get(id=id_of)
            delivery_boy.delete()
            delivery_boys = DeliveryBoyMaster.objects.filter(user=request.user).values("id", "delivery_boy_name", "mobile_number", "area_name__area_name")    
            total_boys = len(delivery_boys)
            data = {"total_boys": total_boys, "delivery_boys": list(delivery_boys)}
            return JsonResponse({"status": 1, "data": data})
        except Exception as e:
            log.exception(e)  
        return JsonResponse({"status": 0})


# ########################################## DRS Master ############################################
@login_required(login_url="login_auth")
def drs(request):
    drs_details = []
    today_drs_details_list = []
    today = datetime.date.today() - timedelta(days=1)
    details = DrsMaster.objects.filter(user=request.user, status="Pending").order_by('-date', '-drs_no')
    for i in details:
        temp_dict = {}
        total_docs = DrsTransactionHistory.objects.filter(drs_number=i.drs_no, user=request.user).count()
        temp_dict["id"] = i.id
        temp_dict["date"] = i.date
        temp_dict["drs_no"] = i.drs_no
        temp_dict["deliveryboy_name"] = i.deliveryboy_name.delivery_boy_name
        temp_dict["total_docs"] = total_docs
        drs_details.append(temp_dict)
    
    today_drs_details = DrsMaster.objects.filter(user=request.user, date__gte=today).order_by('-date', '-drs_no')
    for i in today_drs_details:
        temp_dict = {}
        total_docs = DrsTransactionHistory.objects.filter(drs_number=i.drs_no, user=request.user).count()
        temp_dict["id"] = i.id
        temp_dict["date"] = i.date
        temp_dict["drs_no"] = i.drs_no
        temp_dict["deliveryboy_name"] = i.deliveryboy_name.delivery_boy_name
        temp_dict["total_docs"] = total_docs
        temp_dict["status"] = i.status
        today_drs_details_list.append(temp_dict)

    context = {"drs_details": drs_details, "today_drs_details": today_drs_details_list}    
    return render(request, "drs.html", context=context)


@login_required(login_url="login_auth")
def generate_drs(request):
    area_names = AreaMaster.objects.filter(user=request.user)
    delivery_boy_names = DeliveryBoyMaster.objects.filter(user=request.user)
    # origins = Destination.objects.all()    
    context = {"area_names": area_names, "delivery_boy": delivery_boy_names}
    return render(request, "drs_generate.html", context=context)

@login_required(login_url="login_auth")
def edit_drs_details(request, drs_number):
    try:        
        header = DrsMaster.objects.filter(user=request.user, drs_no=drs_number)                                            
        if header.exists():
            if header[0].status == "Pending":
                drs_details = DrsTransactionHistory.objects.filter(user=request.user, drs_number=drs_number)            
                header = header[0]
                area_names = AreaMaster.objects.filter(user=request.user)
                delivery_boy_names = DeliveryBoyMaster.objects.filter(user=request.user)
                # origins = Destination.objects.all()
                context = {"headers": header, "drs_details": drs_details, "drs_number": drs_number, "area_names": area_names,
                            "delivery_boy": delivery_boy_names}
                return render(request, "edit_drs_details.html", context=context)
            else:
                return redirect("drs")    
        else:
            return redirect("drs")    
    except Exception as e:
        log.exception(e)  
        return redirect("drs")

@login_required(login_url="login_auth")
def doc_num_from_booking_to_drs(request):
    if request.method == "POST":
        doc_num = request.POST.get("docket_num")
        if str(doc_num).isnumeric():
            data = Booking.objects.filter(c_note_number=doc_num)     
            if data.exists():
                data = data.first()
                data = {"name": data.receiver_name, "origin": data.from_destination.name}            
                return JsonResponse({"status": 1, "data": data})
            return JsonResponse({"status": 0})
    return JsonResponse({"status": 0})

@login_required(login_url="login_auth")
def save_drs_details(request):
    if request.method == "POST":
        try:
            drs_history = request.POST.get("drs_history")
            drs_history = ast.literal_eval(drs_history)
            if not drs_history[1:]:
                return JsonResponse({"status": 0, "message": "Empty DRS can't be save."})
            
            area_name = request.POST.get("area_name")        
            area_name = AreaMaster.objects.get(id=area_name)        
            delivery_boy = request.POST.get("delivery_boy_name")        
            delivery_boy = DeliveryBoyMaster.objects.get(id=delivery_boy)            
            drs_date = request.POST.get("drs_date")        
            parcel_status = ParcelStatus.objects.get(name="OUT FOR DELIVERY")

            max_saved_drs_numnber = DrsNoGenerator.objects.filter(user=request.user).aggregate(drs_number=Max("drs_number"))
            if not max_saved_drs_numnber.get("drs_number"):
                max_saved_drs_numnber = 1
            else:
                max_saved_drs_numnber = max_saved_drs_numnber.get("drs_number") + 1     

            
            DrsNoGenerator(user=request.user, drs_number=max_saved_drs_numnber).save()

            DrsMaster(drs_no=max_saved_drs_numnber, date=drs_date, area_name=area_name, 
                      deliveryboy_name=delivery_boy, status="Pending", user=request.user).save()            
            
            instances_to_create = []
            for i in drs_history[1:]:
                instance = DrsTransactionHistory(docket_number=i[0], origin=i[1], consignee_name=i[2], drs_number=max_saved_drs_numnber, status=parcel_status, user=request.user)
                instances_to_create.append(instance)            
            DrsTransactionHistory.objects.bulk_create(instances_to_create)            

            return JsonResponse({"status": 1})
        except:
            return JsonResponse({"status": 0, "message": "select correct details from header."})
    return JsonResponse({"status": 0})

@login_required(login_url="login_auth")
def save_edited_drs_details(request):
    if request.method == "POST":
        try:
            drs_history = request.POST.get("drs_history")
            drs_history = ast.literal_eval(drs_history)
            if not drs_history[1:]:
                return JsonResponse({"status": 0, "message": "Empty DRS can't be save."})
            
            area_name = request.POST.get("area_name")        
            area_name = AreaMaster.objects.get(id=area_name)        
            delivery_boy = request.POST.get("delivery_boy_name")        
            delivery_boy = DeliveryBoyMaster.objects.get(id=delivery_boy)            
            drs_date = request.POST.get("drs_date")        
            parcel_status = ParcelStatus.objects.get(name="OUT FOR DELIVERY")

            max_saved_drs_numnber = request.POST.get("drs_number_new")
            
            # Delete Existing DRS details.
            DrsMaster.objects.get(user=request.user, drs_no=max_saved_drs_numnber).delete()                                
            
            # Save New DRS Details.
            DrsMaster(drs_no=max_saved_drs_numnber, date=drs_date, area_name=area_name, 
                      deliveryboy_name=delivery_boy, status="Pending", user=request.user).save()            
            
            instances_to_create = []
            for i in drs_history[1:]:
                instance = DrsTransactionHistory(docket_number=i[0], origin=i[1], consignee_name=i[2], drs_number=max_saved_drs_numnber, status=parcel_status, user=request.user)
                instances_to_create.append(instance)      

            DrsTransactionHistory.objects.filter(user=request.user, drs_number=max_saved_drs_numnber).delete()
            DrsTransactionHistory.objects.bulk_create(instances_to_create)            

            return JsonResponse({"status": 1})
        except:
            return JsonResponse({"status": 0, "message": "select correct details from header."})
    return JsonResponse({"status": 0})

@login_required(login_url="login_auth")
def delete_drs_details(request):
    if request.method == "POST":
        try:
            sid = request.POST.get("sid")
            data = DrsMaster.objects.get(id=sid, user=request.user)
            data.delete()
            drs_number = data.drs_no
            data1 = DrsTransactionHistory.objects.filter(drs_number=drs_number, user=request.user)
            data1.delete()
            return JsonResponse({"status": 1})
        except:
            return JsonResponse({"status": 0, "message": "DRS not get deleted."})
    return JsonResponse({"status": 0, "message": "DRS not get deleted."})

@login_required(login_url="login_auth")
def upload_drs(request, drs_number):
    try:        
        header = DrsMaster.objects.filter(user=request.user, drs_no=drs_number)                                                    
        if header.exists():
            if header[0].status == "Pending":
                header = header[0]
                delivered_status = ParcelStatus.objects.get(name="DELIVERED")
                all_parcel_status = ParcelStatus.objects.all()
                reasons = Reasons.objects.all()
                drs_history = DrsTransactionHistory.objects.filter(user=request.user, drs_number=header.drs_no)
                context = {"header": header, "delivered_status": delivered_status, "all_parcel_status": all_parcel_status,
                            "drs_history": drs_history, "reasons": reasons}
                return render(request, "drs_upload.html", context=context)
            else:
                return redirect("drs")                
        else:
            return redirect("drs")
    except Exception as e:
        log.exception(e)  
        return redirect("drs")


@login_required(login_url="login_auth")
def upload_drs_details(request):
    if request.method == "POST":
        try:
            drs_history = request.POST.get("drs_history")
            drs_history = ast.literal_eval(drs_history)
            if not drs_history[1:]:
                return JsonResponse({"status": 0, "message": "Empty DRS can't be upload."})
            drs_number = request.POST.get("drs_number")
            header = DrsMaster.objects.get(drs_no=drs_number, user=request.user)
            header.status = "Updated"
            header.save()

            DrsTransactionHistory.objects.filter(user=request.user, drs_number=drs_number).delete()            

            instances_to_create = []
            for i in drs_history[1:]:
                parcel_status = ParcelStatus.objects.get(id=i[3])                
                instance = DrsTransactionHistory(docket_number=i[0], origin=i[1], consignee_name=i[2], drs_number=drs_number, status=parcel_status, user=request.user, reason=i[4])
                instances_to_create.append(instance)
            DrsTransactionHistory.objects.bulk_create(instances_to_create) 

            return JsonResponse({"status": 1})
        except:
            return JsonResponse({"status": 0, "message": "select correct details from header."})
    return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def print_drs(request, drs_number):    
    try:
        drs_header = DrsMaster.objects.get(drs_no=drs_number, user=request.user)
        drs_transaction = DrsTransactionHistory.objects.filter(drs_number=drs_number, user=request.user)[::-1]             
        address = BranchNetwork.objects.get(user=request.user).address     
        branch_name = BranchNetwork.objects.get(user=request.user).branch_name
        return render(request, "drs_print.html", context={"drs_heaser": drs_header,
                                 "drs_history": drs_transaction, "address": address, "branch_name": branch_name})
    
    except Exception as e:
        log.exception(e)  
        return redirect("drs")

@login_required(login_url="login_auth")
def view_drs(request, drs_number):
    try:
        drs_details = DrsMaster.objects.get(user=request.user, drs_no=drs_number)
        if drs_details.status == "Updated":
            drs_history = DrsTransactionHistory.objects.filter(user=request.user, drs_number=drs_number)            
            return render(request, "drs_view.html", context={"header": drs_details, "history": drs_history}) 
        return redirect("drs")
    except Exception as e:      
        log.exception(e)    
        return redirect("drs")

@login_required(login_url="login_auth")
def search_drs_by_num_date(request):
    if request.method == "POST":
        drs_num = request.POST.get("drs_num")
        drs_date = request.POST.get("drs_date")
        if drs_num:
            details = DrsMaster.objects.filter(user=request.user, drs_no=drs_num, status="Updated")
            if details.exists():
                drs_details_list = []
                for i in details:
                    temp_dict = {}
                    total_docs = DrsTransactionHistory.objects.filter(drs_number=i.drs_no, user=request.user).count()
                    temp_dict["id"] = i.id
                    temp_dict["date"] = i.date.strftime("%d-%b-%Y")
                    temp_dict["drs_no"] = i.drs_no
                    temp_dict["deliveryboy_name"] = i.deliveryboy_name.delivery_boy_name
                    temp_dict["total_docs"] = total_docs
                    temp_dict["status"] = i.status
                    drs_details_list.append(temp_dict)                      
                return JsonResponse({"status": 1, "drs_details": drs_details_list})
            return JsonResponse({"status": 0, "message": "DRS Not found for this number."})
        else:            
            details = DrsMaster.objects.filter(user=request.user, date__range=[drs_date, drs_date], status="Updated")
            if details.exists():    
                drs_details_list = []
                for i in details:
                    temp_dict = {}
                    total_docs = DrsTransactionHistory.objects.filter(drs_number=i.drs_no, user=request.user).count()
                    temp_dict["id"] = i.id
                    temp_dict["date"] = i.date.strftime("%d-%b-%Y")
                    temp_dict["drs_no"] = i.drs_no
                    temp_dict["deliveryboy_name"] = i.deliveryboy_name.delivery_boy_name
                    temp_dict["total_docs"] = total_docs
                    temp_dict["status"] = i.status
                    drs_details_list.append(temp_dict)                         
                return JsonResponse({"status": 1, "drs_details": drs_details_list})
            return JsonResponse({"status": 0, "message": "DRS Not found for this date."})

    return redirect("drs")

# ############################## Manifest details here ###################################
@login_required(login_url="login_auth")
def manifest_show(request):
    today = datetime.date.today() #- timedelta(days=1)
    status = ParcelStatus.objects.get(name="OUT")    
    # data = Trackinghistory.objects.filter(user=request.user, status=status, in_out_datetime__gt=today).annotate(date_substr=Substr('in_out_datetime', 1, 10)).values("d_to__name", "date_substr", "d_to__id").annotate(child_count=Count('d_to')).order_by("-date_substr")        
    data = Trackinghistory.objects.filter(user=request.user, status=status, in_out_datetime__gt=today).annotate(date_substr=TruncDate('in_out_datetime')).values("d_to__name", "date_substr", "d_to__id").annotate(child_count=Count('d_to')).order_by("-date_substr")    
    return render(request, "manifest.html", context={"details": data})


@login_required(login_url="login_auth")
def search_manifest(request):
    if request.method == "POST":
        date = request.POST.get("date")
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        next_date = date + timedelta(days=1)        
        status = ParcelStatus.objects.get(name="OUT")    
        # data = Trackinghistory.objects.filter(user=request.user, status=status, in_out_datetime__range=[date, next_date]).annotate(date_substr=Substr('in_out_datetime', 1, 10)).values("d_to__name", "date_substr", "d_to__id").annotate(child_count=Count('d_to')).order_by("-date_substr")        
        data = Trackinghistory.objects.filter(user=request.user, status=status, in_out_datetime__range=[date, next_date]).annotate(date_substr=TruncDate('in_out_datetime')).values("d_to__name", "date_substr", "d_to__id").annotate(child_count=Count('d_to')).order_by("-date_substr")        
        if data.exists():            
            return JsonResponse({"status": 1, "data": list(data)})
        return JsonResponse({"status": 0, "message": "Manifest not found for selected date."})
    return JsonResponse({"status": 0, "message": "Get method is not allowed."})


@login_required(login_url="login_auth")
def print_manifest(request, sid_num):
    try:
        sid_details = str(sid_num).split("_")
        destination = sid_details[0]
        destination = Destination.objects.get(id=destination)
        date = sid_details[1]
        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")    
        except:
            log.info("{}".format(date))
            date = datetime.datetime.strptime(date, "%b. %d, %Y")    
        next_date = date + timedelta(days=1)       
        status = ParcelStatus.objects.get(name="OUT")    
        data = Trackinghistory.objects.filter(user=request.user, status=status, in_out_datetime__range=[date, next_date], d_to=destination)                
        user_details = BranchNetwork.objects.get(user=request.user)
        # print(user_details.branch_incharge_number, user_details.office_lane_line_number)
        context = {"data": data, "user_details": user_details, "date": date, "destination": destination}        
        return render(request, "manifest_print.html", context=context)
    except Exception as e:
        log.exception(e)
        return redirect("manifest_show")
    
# ######################################## C Note Details for admi use only #################################

@login_required(login_url="login_auth")
def c_note_master(request):
    log.info("Request for C Note Number by {}".format(request.user))
    user_details = UserAdditionalDetails.objects.get(user=request.user)
    last_number = CNoteGenerator.objects.aggregate(max_value=Max("to_range"))["max_value"]
    if not last_number:
        last_number = 2121110    
    from_range = last_number + 1
    to_range = from_range + 99
    last_50_records = CNoteGenerator.objects.order_by('-created_at')[:50]
    users = User.objects.all()    
    # print(i.id, i.username)
    context= {
        "last_number": last_number,
        "from_range": from_range,
        "to_range": to_range,
        "last_50_records": last_50_records,
        "users": users
    }
    return render(request, "c_note_master.html", context=context)

@login_required(login_url="login_auth")
def save_c_note_number(request):
    if request.method == "POST":
        try:
            user = request.POST.get("user")
            from_range = request.POST.get("from_range")
            to_range = request.POST.get("to_range")
            result = int(to_range) - int(from_range)
            if result >= 1:                        
                user = User.objects.get(id=user)                        
                CNoteGenerator(from_range=from_range, to_range=to_range, user=user).save()
                return JsonResponse({"status":1})            
            return JsonResponse({"status": 0, "message": "C. Note Number can't be less than last assign number"})        
        except Exception as e:
            log.exception(e)
    return JsonResponse({"status": 0})

@login_required(login_url="login_auth")
def delete_c_note_details(request):
    if request.method == "POST":
        try:
            sid = request.POST.get("sid")
            CNoteGenerator.objects.get(id=sid).delete()            
            return JsonResponse({"status": 1})
        except Exception as e:
            log.exception(e)
    return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def retutn_all_foreign_key_details(request):
    if request.method == "POST":
        booking_type = BookingType.objects.all().values("id", "booking_type").order_by("booking_type")
        ref_courier_names = RefCourier.objects.all().values("id", "name").order_by("name")
        destinations = Destination.objects.all().values("id", "name").order_by("name")
        state = State.objects.all().values("id", "state_name").order_by("state_name")
        # part_master = PartyAccounts.objects.filter(user=request.user).values("id", "party_name").order_by("party_name")    
        return JsonResponse({"status": 1,"booking_type": list(booking_type), "ref_courier_names": list(ref_courier_names),
                            "destinations": list(destinations), "state": list(state)})

    return JsonResponse({"status": 0})


def shipment_book(request):    
    if request.method == "POST":        
        s_name = request.POST.get("sender_name")
        s_mob = request.POST.get("sender_mob")
        s_pincode = request.POST.get("sender_pincode")
        s_address = request.POST.get("sender_address")
        r_name = request.POST.get("receiver_name")
        r_mob = request.POST.get("receiver_mob")
        r_pincode = request.POST.get("receiver_pincode")
        r_address = request.POST.get("receiver_address")
        p_weight = request.POST.get("weight")
        p_lenght = request.POST.get("lenght")
        p_breadth = request.POST.get("breadth")
        p_hieght = request.POST.get("height")
        p_item = request.POST.get("item_desc")
        p_remarks = request.POST.get("remarks")
        p_pickup = request.POST.get("pickup_date")        
        branch_aloted = False
        branch_available = BranchNetwork.objects.filter(pincode=s_pincode)
        if branch_available.exists():
            branch_available = branch_available[0].user   
            branch_aloted = True         
        else:
            branch_available = Network.objects.filter(pincode=s_pincode)
            if branch_available.exists():
                branch_available = branch_available[0].user    
                branch_aloted = True
            else:
                branch_available = User.objects.get(is_superuser=True)                        
        client_ip = request.META.get('REMOTE_ADDR', None)
        log.info("User try to book shipment for Pincode: {} - (DIY journey).IP: {}".format(r_pincode, client_ip))
        UserBooking(s_name=s_name, s_mob=s_mob, s_pincode=s_pincode, s_address=s_address,
                    r_name=r_name, r_mob=r_mob, r_pincode=r_pincode, r_address=r_address,
              p_weight=p_weight, p_lenght=p_lenght, p_breadth=p_breadth, p_hieght=p_hieght,
              p_item=p_item, p_remarks=p_remarks, p_pickup=p_pickup, status="OPEN",
                assign_user=branch_available, pick_up=False, ip_address=client_ip,
                branch_aloted=branch_aloted).save()   
            
        return render(request, 'user_book.html', context={"return_message": "Congratulations! Your details have been submitted successfully, Our team will contact you shortly."})
    marquee_message = get_marque_message()
    return render(request, 'user_book.html', context={"marque_message": marquee_message})

