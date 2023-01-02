from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Booking, Trackinghistory
import base64
import requests
import datetime

# Create your views here.
def home(request):   
    today_date = datetime.datetime.now().strftime("%Y")
    if request.method == "POST":
        tracking_id = request.POST.get("tracking_number")                
        if tracking_id:                                    
            return redirect("/tracking/{}".format(tracking_id))    
    return render(request, "index.html", {"today_date": today_date})    


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
                    url = str(booking_details.ref_courier_name.link) + str(booking_details.ref_courier_number)
                    response = requests.post(url, headers={"content-type": "application/json"})
                    data_load_from_another_site = response.json()                    
                    last_status = data_load_from_another_site.get("MostRecentStatus", "-")
                    tracking_history = data_load_from_another_site.get("Checkpoints", "")                    

                return render(request, "tracking.html", {"booking_details": booking_details, "tracking_history": tracking_history,
                "last_status": last_status})   

        return redirect("home")
    except Exception as e:
        print(e.__str__())                
        return redirect("home")



