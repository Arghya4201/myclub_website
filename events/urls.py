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
]
