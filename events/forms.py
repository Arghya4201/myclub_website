from django import forms
from django.forms import ModelForm
from .models import Venue


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
