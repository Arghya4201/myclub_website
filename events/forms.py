from django import forms
from django.forms import ModelForm
from .models import Venue, Event


# Create a venue form
# Readme_myClubWebsite5
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        # fields = '__all__'
        fields = ("name", "address", "zip_code", "phone", "web", "email")

        labels = {
            # Setting all the labels as nothing so nothing will pop above the input boxes
            "name": "",
            "address": "",
            "zip_code": "",
            "phone": "",
            "web": "",
            "email": "",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Venue Name"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
            "zip_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ZipCode"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "web": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Website Address"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email Address"}
            ),
        }

#This form is for superuser (can assign manager to any user)
class EventFormAdmin(ModelForm):
    class Meta:
        #Defines the model where this form data would go
        model = Event
        fields = "__all__"

        labels = {
            "name": "",
            "event_date": "",
            "venue": "Venue",
            "attendees": "Attendees",
            "manager": "Manager",
            "description": "",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Event Name"}
            ),
            "event_date": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Event Date"}
            ),
            "venue": forms.Select(attrs={"class": "form-select"}),
            "attendees": forms.SelectMultiple(attrs={"class": "form-select"}),
            "manager": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
        }

#FOr normal user who wants to create an event (automatically assigned manager as logged in user)
class EventForm(ModelForm):
    class Meta:
        #Defines the model where this form data would go
        model = Event
        fields = ('name', 'event_date', 'venue', 'attendees', 'description')

        labels = {
            "name": "",
            "event_date": "",
            "venue": "Venue",
            "attendees": "Attendees",
            "description": "",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Event Name"}
            ),
            "event_date": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Event Date"}
            ),
            "venue": forms.Select(attrs={"class": "form-select"}),
            "attendees": forms.SelectMultiple(attrs={"class": "form-select"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
        }