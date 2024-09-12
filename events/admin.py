from django.contrib import admin
from .models import Event
from .models import Venue
from .models import MyClubUser
from django.contrib.auth.models import Group

# Register your models here.

# admin.site.register(Event)
# admin.site.register(Venue)
admin.site.register(MyClubUser)

#Uregistering the Group model
admin.site.unregister(Group)
# Readme_myClubWebsite4
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'zip_code')
    ordering = ('name',)
    search_fields = ('name', 'address')
  
@admin.register(Event)
#Making changes to the EventAdmin page
class EventAdmin(admin.ModelAdmin):
    #Fields to be displayed on the EventAdmin page
    fields = (('name', 'venue'), 'event_date', 'description', 'manager','attendees')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    #Ordering in descending order wrt event_date
    ordering = ('-event_date',)
    search_fields = ('name', 'description')


 
