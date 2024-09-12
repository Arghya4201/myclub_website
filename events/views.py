from django.contrib import messages
from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.contrib.auth.models import User
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect,HttpResponse
import csv

#IMPORT PDF STUFFS
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#IMPORT PAGINATOR STUFFS
from django.core.paginator import Paginator

# Create your views here.

#NOT WORKING
def venues_pdf(request):
    #Create bytestream buffer
    buf = io.BytesIO()
    #create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #create text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    #Add some lines of text
    #lines = ['First line of text', 'Second line of text', 'Third line of text']
    #for line in lines:
    #    textob.textLine(line)
    venues = Venue.objects.all()

    lines = []
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email)
        lines.append("\n")
     
    #Loop through the list and append in pdf file one by one    
    for line in lines:
        textob.textLine(line)

    #Finish
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')

#Generate text file for venue list
def venues_text(request):
    Venues = Venue.objects.all()
    response = HttpResponse(content_type='text/plain')
    #This line would download the file in our local computer
    response['content-disposition'] = 'attachment; filename=venues.txt'
    #A blank list
    list = []
    for venue in Venues:
        list.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email}\n\n')
    response.writelines("%s\n" % venue for venue in list)
    return response

#Venue CSV file generate
def venues_csv(request):
    venues = Venue.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=venues.csv'
    #Create a csv writer object
    writer = csv.writer(response)
    writer.writerow(['Name', 'Address', 'Zip Code', 'Phone', 'Web', 'Email'])
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email])
    return response

def admin_approval(request):
    events = Event.objects.all()
    if request.user.is_superuser:
        # return render(request, "events/admin_approval.html", {"events": events})
        if request.method == "POST":
            id_list = request.POST.getlist("Boxes")
            # print(id_list)
            #Unchecking all the boxes before checking because value gets passed only when we check boxes , nothing gets passed on unchecking
            #checking those ids
            Event.objects.update(approved=False)
            for id in id_list:
                Event.objects.filter(pk=int(id)).update(approved=True)
            messages.success(request, "Event Approved Successfully", extra_tags="success")
            return redirect("list-events")
        else:
            return render(request, "events/admin_approval.html", {"events": events})
    else:
        messages.error(request, "You are not authorized to view this page", extra_tags="warning")
        return redirect("list-events")    
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect("list-venues")

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager or request.user.is_superuser:
        event.delete()
        messages.success(request, "Event Deleted Successfully", extra_tags="success")
    else:
        messages.error(request, "You are not authorized to delete this event", extra_tags="warning")
    return redirect("list-events")
def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/add_event?submitted=True")
        else:
            form = EventForm(request.POST)
            #storing the event by taking value from forms but not yet commiting it
            event = form.save(commit=False)
            # setting manager as the current logged user
            event.manager = request.user
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/add_event?submitted=True")
    else:
        # form  = EventForm()
        #Just going to the page not submitted
        if request.user.is_superuser:
            form = EventFormAdmin()
        else:
            form = EventForm()
        if "submitted" in request.GET:
            submitted = True
    return render(
        request, "events/add_event.html", {"form": form, "submitted": submitted}
    )
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect("list-events")
    return render(request, "events/update_event.html", {"event": event, "form": form})

def update_venues(request,venue_id):
    venue = Venue.objects.get(pk=venue_id)
    # Readme_myClubWebsite8
    form = VenueForm(request.POST or None,request.FILES or None , instance=venue)
    if(form.is_valid()):
        form.save()
        return redirect('list-venues')
    return render(request, "events/update_venue.html", {"venue": venue, "form": form})

def search_venues(request):
    if(request.method == "POST"):
        #Using POST instead of GET because we are getting data from the form and not from the URL
        #Searched is the name of the input in the form (see navbar.html the from tag above the search input tag)
        searched = request.POST["searched"]
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, "events/search_venues.html", {"searched": searched, "venues": venues})
    else:
        return render(request, "events/search_venues.html", {})
 
def search_events(request):
    if(request.method == "POST"):
        searched = request.POST["searched"]
        events = Event.objects.filter(name__contains=searched)
        return render(request, "events/search_events.html", {"searched": searched, "events": events})
    else:
        return render(request, "events/search_events.html", {})    
    
def show_venue(request, venue_id):
    #Readme_myClubWebsite7
    venue = Venue.objects.get(pk=venue_id)
    #Getting the Username from the user model referencing the primary key from the venue model
    #This is a query an now we can also access the other attributes of that user like the user mail, last_name ,etc By writing venue_owner.email in the html page
    venue_owner = User.objects.get(pk=venue.Owner)
    return render(request, "events/show_venue.html", {"venue": venue, "venue_owner": venue_owner})
    
def list_venues(request):
    venue_list = Venue.objects.all().order_by("name")
    p = Paginator(venue_list, 2)
    page = request.GET.get('page')
    venues_paginated = p.get_page(page)
    return render(request, "events/venue.html", {"venues": venue_list, "venues_paginated": venues_paginated})

# Readme_myClubWebsite6
def add_venue(request):
    submitted = False
    if request.method == "POST":
        #Creating an object of the VenueForm class
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.Owner = request.user.id
            form.save()
            return HttpResponseRedirect("/add_venue?submitted=True")
    else:
        form = VenueForm()
        if "submitted" in request.GET:
            submitted = True
    return render(
        request, "events/add_venue.html", {"form": form, "submitted": submitted}
    )

def my_events(request):
    if request.user.is_authenticated:
        current_user = request.user.id
        event_list = Event.objects.filter(attendees=current_user)
        return render(request, "events/my_events.html", {"event_list": event_list})
    else:
        messages.error(request, "You need to be logged in to view your events", extra_tags="warning")
        event_list = Event.objects.all().order_by("-event_date")
        return render(request, "events/event_list.html", {"event_list": event_list})
def all_events(request):
    event_list = Event.objects.all().order_by("-event_date")
    return render(request, "events/event_list.html", {"event_list": event_list})


# The request parameter is the defaultURL, the rest year and month are passed extra in the pathURL like request/<year>/<month> eg: localhost:8000/2021/01
def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    name = "Arghya"
    month = month.capitalize()

    # Convert month name to number
    month_number = list(calendar.month_name).index(month)
    if month_number == 0:
        raise ValueError("Invalid month name")
    month_number = int(month_number)

    # get current year
    now = datetime.now()
    current_year = now.year

    # get current month
    current_month = now.strftime("%B")

    # get current date
    current_date = now.day

    # Get current time
    current_time = now.strftime("%H:%M:%S")

    # Create the calendar
    calendar_instance = HTMLCalendar()  # Create an instance of HTMLCalendar
    cal = calendar_instance.formatmonth(year, month_number)
    
    #Querying Events based on current year and month
    events = Event.objects.filter(event_date__year=year, event_date__month=month_number)

    # templates folder is at same level as our appName i.e events, so we write (this events is the one inside template) events/home.html as file location is templates->events->home.html. Here we point to the page what we want to render
    return render(
        request,
        "events/home.html",
        {
            "name": name,
            "year": year,
            "month": month,
            "month_number": month_number,
            "cal": cal,
            "current_year": current_year,
            "current_date": current_date,
            "current_month": current_month,
            "time": current_time,
            "events": events
        },
    )
