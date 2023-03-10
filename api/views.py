"""
Some of basic django imports that help to render and filter data from database.
"""
import base64
import requests
import datetime
# import test_api
from .test_api import get_search_details
from datetime import timedelta
from django.db.models import Q
from .models import Booking, ParcelStatus, Trackinghistory, UserAdditionalDetails
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import contactus, Token, BranchNetwork, Destination
from .models import RefCourier, PartyAccounts
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import threading


today_date = datetime.datetime.now().strftime("%Y")
# Create your views here.
def home(request):  
    """
    Thi function returns to home page.
    """         
    if request.method == "POST":
        tracking_id = request.POST.get("tracking_number")                
        if tracking_id:                                    
            return redirect("/tracking/{}".format(tracking_id))    
    return render(request, "index.html", {"today_date": today_date, "return_message": None})    


def tracking(request, tracking_number):    
    try:            
        tracking_number = int(tracking_number)        
        if tracking_number:
            data = Booking.objects.filter(c_note_number=tracking_number)            
            if data:
                booking_details = data[0]                    
                tracking_history = Trackinghistory.objects.filter(c_note_number=booking_details).order_by('-in_out_datetime')                                                                                        
                # print(booking_details.c_note_number, booking_details.from_destination,
                # booking_details.to_destination, booking_details.doc_date.strftime("%d-%b-%Y %H:%M %p"), booking_details.receiver_name)                                    
                last_status = "Shipment information sent to Airpost Xpress"
                if tracking_history:                    
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
                            url = f'For latest updates click on this Ref No. <a id="sele_data" class="text-primary sele_data_1" data-sid="{url}" >{booking_details.c_note_number}</a>'
                        else:
                            url = f'For latest updates click on this Ref No. <a href="{url}" target="_blank">{booking_details.c_note_number}</a>'
                        tracking_history["Date"] = ""
                        tracking_history["Location"] = ""
                        tracking_history["CheckpointState"] = ""
                        tracking_history["Activity"] = url
                        tracking_history = [tracking_history,]
                return render(request, "tracking.html", {"booking_details": booking_details, "tracking_history": tracking_history,
                "last_status": last_status})   

        return redirect("home")        
    except Exception as e:   
        print(e)                    
        return redirect("home")


def tracking_with_selenium(request, details):
    # def start_in_thread():
    final_data = str(details).split("UUUU")
    courier = final_data[0]
    doc_number = final_data[1]    
    data = get_search_details(courier=courier, doc_number=doc_number)

    return JsonResponse({"status": 1, "data": data})
    # threading.Thread(target=start_in_thread).start()


def contactUs(request):    
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        country = request.POST.get("country")
        pincode = request.POST.get("pincode")
        message = request.POST.get("message")
        if name and email and country and pincode:            
            contact_obj = contactus.objects.create(name=name, email=email, country=country, mobile_number=pincode, message=message)
            contact_obj.save()
            return_message = "Request submitted successfully."       

            return render(request, "contactus.html", {"return_message": return_message})
        else:
            print("Pending...")


    return render(request, "contactus.html")

def network(request):
    message = 1    
    head_offices = BranchNetwork.objects.filter(status="R O")            
    if request.method == "POST":
        if "by_pincode" in request.POST and request.POST.get("pincode"):
            pincode = request.POST.get("pincode")
            data = BranchNetwork.objects.filter(pincode=pincode)          
            if data:                                              
                message = None
                context = {"head_offices": head_offices, "message": None, "data": data}

                return render(request, "network.html", context=context)
            else:
                context = {"head_offices": head_offices, "message": 1}

                return render(request, "network.html", context=context)
        
        elif "by_area" in request.POST and request.POST.get("area_name"):
            area_name = request.POST.get("area_name")           
            ques = (Q(branch_name__icontains=area_name) | Q(state__state_name__icontains=area_name) 
            | Q(zone__name__icontains=area_name) | Q(area_name__icontains=area_name))
            data = BranchNetwork.objects.filter(ques)
            if data:                                              
                message = None
                context = {"head_offices": head_offices, "message": None, "data": data}
                return render(request, "network.html", context=context)
            else:
                context = {"head_offices": head_offices, "message": 1}
                return render(request, "network.html", context=context)            
        
        else:
            context = {"head_offices": head_offices, "message": 1}
            return render(request, "network.html", context=context)

    message = None
    context = {"head_offices": head_offices, "message": message}
    return render(request, "network.html", context=context)


def services(request):
    return render(request, "services.html")


def about_us(request):
    return render(request, "aboutus.html")


def login_auth(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=user_name, password=password)
        if user:
            auth.login(request, user)
            return redirect("dashboard")
        else:
            context = {"message": "Invalid credentials !"}
            return render(request, "login.html", context)
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("login_auth")


@login_required(login_url="login_auth")
def dashboard(request):
    
    return render(request, "dashboard.html")

# ###############################3 Dashboard details #####################################

@login_required(login_url="login_auth")
def bookings(request):    
    destinations = Destination.objects.all()    
    ref_courier_name = RefCourier.objects.all()    
    parties = PartyAccounts.objects.filter(user=request.user)
    today_date = datetime.date.today()    
    today_bookings = Booking.objects.filter(created_at__startswith=today_date, user=request.user).order_by("-created_at")    
    context = {"destinations": destinations, 
               "ref_courier_name": ref_courier_name,
               "parties": parties, "today_bookings": today_bookings,
               "total_bookings": len(today_bookings)}                
    return render(request, "bookings.html", context=context)


@login_required(login_url="login_auth")
def save_booking(request):
    if request.method == "POST":        
        update_id = request.POST.get("id")                      
        c_note_number = request.POST.get("cnotenumber")
        existing_c_note = Booking.objects.filter(c_note_number=c_note_number)
        request.session["success"] = None
        request.session["next_c_note"] = ""
        party_name = request.POST.get("party")        
        party_name = PartyAccounts.objects.get(id=party_name)
        booking_datetime = request.POST.get("datetime")        
        from_dest = request.POST.get("from_destination")
        from_dest = Destination.objects.get(id=from_dest)
        to_dest = request.POST.get("todest")
        to_dest = Destination.objects.get(id=to_dest)
        s_name = request.POST.get("s_name")
        s_number = request.POST.get("s_number")
        r_name = request.POST.get("r_name")
        r_number = request.POST.get("r_number")        
        ref_courier = request.POST.get("ref_courier")        
        ref_courier = RefCourier.objects.get(id=ref_courier)
        ref_number = request.POST.get("ref_number")
        if not update_id:            
            if not existing_c_note:                            
                booking_obj = Booking.objects.create(doc_date=booking_datetime, party_name=party_name,
                c_note_number=c_note_number, from_destination=from_dest, to_destination=to_dest,
                sender_name=s_name, sender_mobile=s_number, receiver_name=r_name, receiver_mobile_number=r_number,
                ref_courier_name=ref_courier, ref_courier_number=ref_number, user=request.user)                    
                booking_obj.save()            
                request.session["success"] = "success"
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
            booking_obj.c_note_number = c_note_number
            booking_obj.from_destination = from_dest
            booking_obj.to_destination = to_dest
            booking_obj.sender_name = s_name
            booking_obj.sender_mobile = s_number
            booking_obj.receiver_name = r_name
            booking_obj.receiver_mobile_number = r_number
            booking_obj.ref_courier_name = ref_courier
            booking_obj.ref_courier_number = ref_number 
            booking_obj.user=request.user                    
            booking_obj.save()            
            request.session["success"] = "success"
            messages.success(request, "Shipment updated Successfully.")
            return redirect("bookings")
        # print("party_name: ", party_name, "booking_datetine:", booking_datetime,
        # "c_note_number: ", c_note_number, "from_dest: ", from_dest,
        # "To_dest: ", to_dest, "s_name: ", s_name, "s_number: ", s_number, "r_name: ", r_name, 
        # "r_number: ", r_number, "ref_courier: ", ref_courier, "ref_numbe: ", ref_number)                
    return redirect("bookings")

@login_required(login_url="login_auth")
def edit_data_retrive(request):
    if request.method == "POST":
        id = request.POST.get("id")        
        data = Booking.objects.filter(pk=id).values("id", "doc_date", "party_name", "c_note_number", 
        "from_destination", "to_destination", "sender_name", "sender_mobile", "receiver_name", "receiver_mobile_number",
        "ref_courier_name", "ref_courier_number")              
        return JsonResponse({"data": list(data)})


@login_required(login_url="login_auth")
def advance_search_by_date(request):
    if request.method == "POST":
        from_date =  request.POST.get("from_date")
        to_date =  request.POST.get("to_date")

        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
        to_date = to_date + timedelta(days=1)        
        data = Booking.objects.filter(doc_date__range=(from_date, to_date), user=request.user).values("id", "c_note_number", "to_destination__name", "ref_courier_name__name")        
        if data:            
            return JsonResponse({"status": 1, "data": list(data)})
        else:
            return JsonResponse({"ststua": 0})
    else:
        return JsonResponse({"ststua": 0})
        

@login_required(login_url="login_auth")
def advance_search_by_c_note(request):
    if request.method == "POST":
        c_note_number =  request.POST.get("c_note_number")                
        data = Booking.objects.filter(c_note_number=c_note_number, user=request.user).values("id", "c_note_number", "to_destination__name", "ref_courier_name__name")
        if data:            
            return JsonResponse({"status": 1, "data": list(data)})
        else:
            return JsonResponse({"ststua": 0})
    else:
        return JsonResponse({"ststua": 0})


@login_required(login_url="login_auth")
def advance_search_for_ref_number(request):
    if request.method == "POST":
        ref_number =  request.POST.get("ref_number")                
        data = Booking.objects.filter(ref_courier_number=ref_number, user=request.user).values("id", "c_note_number", "to_destination__name", "ref_courier_name__name")
        if data:            
            return JsonResponse({"status": 1, "data": list(data)})
        else:
            return JsonResponse({"ststua": 0})
    else:
        return JsonResponse({"ststua": 0})


# ############################# Party Details start ###################################################

@login_required(login_url="login_auth")
def part_master(request):
    parties = PartyAccounts.objects.filter(user=request.user)
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

        parties = PartyAccounts.objects.filter(user=request.user)
        total_parties = len(parties)
        context = {"parties": parties, "total_parties": total_parties}  

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
            print(e)
            return JsonResponse({"status": 0})


@login_required(login_url="login_auth")
def delete_party_detail(request):
    id_of = request.POST.get("id")
    try:
        data = PartyAccounts.objects.get(id=id_of)
        data.delete()        
        data = PartyAccounts.objects.values()      
        total_parties = len(data)        
        return JsonResponse({"status": 1, "data": list(data), "total_parties": total_parties})

    except Exception as e:
        print(e)


# ############################## TRACKING HOSTORY IN start ##########################################

@login_required(login_url="login_auth")
def tracking_history_in(request):
    destinations = Destination.objects.all()
    today_date = datetime.date.today()    
    status = ParcelStatus.objects.get(name="IN")  
    today_in = Trackinghistory.objects.filter(user=request.user, last_updated_datetime__startswith=today_date, status=status).order_by("-last_updated_datetime")
    context = {"destinations": destinations, "doc_in": today_in}    
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
                        from_destination = Destination.objects.get(id=from_destination)                        
                        if id_of:
                            saved_data = Trackinghistory.objects.get(id=id_of)
                            saved_data.c_note_number = c_note_number_booking
                            saved_data.remarks = remarks
                            saved_data.d_from = to_destination
                            saved_data.in_out_datetime = date
                            saved_data.save()                                               
                        else:
                            Trackinghistory.objects.create(c_note_number=c_note_number_booking, in_out_datetime=date,
                                    d_from=to_destination, d_to=to_destination, status=status, remarks=remarks, user=user)                                                
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
    destinations = Destination.objects.all()
    today_date = datetime.date.today()    
    status = ParcelStatus.objects.get(name="OUT")
    today_in = Trackinghistory.objects.filter(user=request.user, last_updated_datetime__startswith=today_date, status=status).order_by("-last_updated_datetime")
    context = {"destinations": destinations, "doc_in": today_in}    
    return render(request, "tracking_history_out.html", context=context)


@login_required(login_url="login_auth")
def save_output_load(request):
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
                            Trackinghistory.objects.create(c_note_number=c_note_number_booking, in_out_datetime=date,
                                    d_from=to_destination, d_to=from_destination, status=status, remarks=remarks, user=user)                                                
                        # data = Trackinghistory.objects.values()
                        today_date = datetime.date.today()      
                        today_in = Trackinghistory.objects.filter(user=request.user, last_updated_datetime__startswith=today_date, status=status).order_by("-last_updated_datetime")
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
            data = Trackinghistory.objects.filter(user=request.user, c_note_number=c_note_number, status=status).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_from__name", "remarks")        
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
            data = Trackinghistory.objects.filter(user=request.user, c_note_number=ref_number, status=status).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_from__name", "remarks")                    
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
                                              status=status).values("id", "c_note_number__c_note_number", "in_out_datetime", "d_from__name", "remarks")        
        return JsonResponse({"status": 1, "data": list(data)})
    else:
        return JsonResponse({"status": 0})