from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #Path Converter (Now we can access the Home page by defaultURL/year/month eg: localhost:8000/2021/01)
    path('',views.home, name='home'),
    path('<int:year>/<str:month>',views.home, name='home'),
    path('events',views.all_events, name='list-events'),
    path('add_venue',views.add_venue, name='add-venue'),
    path('list_venues',views.list_venues, name='list-venues'),
    path('show_venue<venue_id>',views.show_venue, name='show-venue'),
    path('search_venues',views.search_venues, name='search-venues'),
    path('update_venues<venue_id>',views.update_venues,name='update-venue'),
    path('update_event<event_id>',views.update_event,name='update-event'),
    path('add_event',views.add_event, name='add-event'),
    path('delete_event<event_id>',views.delete_event, name='delete-event'),
    path('delete_venue<venue_id>',views.delete_venue, name='delete-venue'),
    path('venues-text',views.venues_text, name='venues-text'),
    path('venues_csv',views.venues_csv, name='venues-csv'),
    path('venues-pdf',views.venues_pdf, name='venues-pdf'),
    path('my_events',views.my_events, name='my-events'),
    path('search_events',views.search_events, name='search-events'),
    path('admin_approval',views.admin_approval,name='admin-approval'),
    path('venue_events<venue_id>',views.venue_events, name='venue-events')
]
