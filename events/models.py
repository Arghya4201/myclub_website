from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Venue(models.Model):
    name = models.CharField("Venue Name", max_length=100)
    address = models.CharField(max_length=300)
    zip_code = models.CharField("Zip Code", max_length=15)
    phone = models.CharField("Contact Phone", max_length=25, blank=True)
    web = models.URLField("Website Address",blank=True)
    email = models.EmailField("Email Address",blank=True)
    Owner = models.IntegerField("Venuw Owner", blank=True, null=True, default=1)
    venue_images = models.ImageField(null=True, blank=True, upload_to="images/")


    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField("User Email")


    def __str__(self):
        return self.first_name + " " + self.last_name


class Event(models.Model):
    name = models.CharField(max_length=100)
    event_date = models.DateField()
    # Connect Event table with Venue table
    # Readme_myClubWebsite3
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(MyClubUser, blank=True)
    # manager = models.CharField(max_length=100)
    # Readme_myClubWebsite4
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    #Unapproved By default
    approved = models.BooleanField('Approved',default=False)


    def __str__(self):
        return self.name
    
    #Not adding the property to the model but just creating a property hence no need to make migrations as its not actually getting stored in db
    @property
    def Date_till(self):
        today = datetime.now().date()
        date_till_event = self.event_date - today
        date_till_event_stripped = str(date_till_event).split(",",1)[0]
        return date_till_event_stripped
