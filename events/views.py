from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm
from django.http import HttpResponseRedirect


# Create your views here.
def show_venue(request, venue_id):
    #Readme_myClubWebsite7
    venue = Venue.objects.get(pk=venue_id)
    return render(request, "events/show_venue.html", {"venue": venue})
    
def list_venues(request):
    venue_list = Venue.objects.all()
    return render(request, "events/venue.html", {"venues": venue_list})

# Readme_myClubWebsite6
def add_venue(request):
    submitted = False
    if request.method == "POST":
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
    event_list = Event.objects.all()
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
