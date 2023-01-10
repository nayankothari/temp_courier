"""
Some of basic django imports that help to render and filter data from database.
"""
import base64
import requests
import datetime
from django.db.models import Q
from .models import Booking, Trackinghistory
from django.shortcuts import render, redirect
from .models import contactus, Token, BranchNetwork
from django.http import HttpResponse, HttpResponseRedirect


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
                    except Exception as e:
                        print(e.__str__())
                        pass

                return render(request, "tracking.html", {"booking_details": booking_details, "tracking_history": tracking_history,
                "last_status": last_status})   

        return redirect("home")
    except Exception as e:
        print(e.__str__())                
        return redirect("home")



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