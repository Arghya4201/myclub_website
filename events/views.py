from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm
from django.http import HttpResponseRedirect,HttpResponse


# Create your views here.

#Generate text file for venue list
def venues_text(request):
    Venues = Venue.objects.all()
    response = HttpResponse(content_type='text/plain')
    #A blank list
    list = []
    for venue in Venues:
        list.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email}\n\n')
    response.writelines("%s\n" % venue for venue in list)
    return response
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect("list-venues")

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect("list-events")
def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/add_event?submitted=True")
    else:
        form = EventForm()
        if "submitted" in request.GET:
            submitted = True
    return render(
        request, "events/add_event.html", {"form": form, "submitted": submitted}
    )
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect("list-events")
    return render(request, "events/update_event.html", {"event": event, "form": form})

def update_venues(request,venue_id):
    venue = Venue.objects.get(pk=venue_id)
    # Readme_myClubWebsite8
    form = VenueForm(request.POST or None , instance=venue)
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
    
def show_venue(request, venue_id):
    #Readme_myClubWebsite7
    venue = Venue.objects.get(pk=venue_id)
    return render(request, "events/show_venue.html", {"venue": venue})
    
def list_venues(request):
    venue_list = Venue.objects.all().order_by("name")
    return render(request, "events/venue.html", {"venues": venue_list})

# Readme_myClubWebsite6
def add_venue(request):
    submitted = False
    if request.method == "POST":
        #Creating an object of the VenueForm class
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/add_venue?submitted=True")
    else:
        form = VenueForm()
        if "submitted" in request.GET:
            submitted = True
    return render(
        request, "events/add_venue.html", {"form": form, "submitted": submitted}
    )


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
        },
    )
