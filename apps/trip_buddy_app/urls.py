from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), # html 1 - index (login)
    url(r'^dashboard$', views.dashboard), # html 2 - dashboard
    url(r'^trips/edit/(?P<trip_id>\d+)$', views.edit_trip), # html 3 - edit
    url(r'^trips/new$', views.new_trip), # html 4 - add a new trip
    url(r'^trips/(?P<trip_id>\d+)$', views.view_trip), # html 5 - view trip detail

    url(r'^register$', views.register), # method 1 - register (from login page)
    url(r'^login$', views.login), # method 2- login
    url(r'^logout$', views.logout), # method 3 - logout
    
    url(r'^trips/delete/(?P<trip_id>\d+)$', views.delete_trip), # method 4 - delete a trip (from dashboard link)
    # url(r'^edit/(?P<trip_id>\d+)$', views.edit_trip), # method 5 - to edit page

    url(r'^trips/join/(?P<trip_id>\d+)$', views.join_trip),# method 5.1 - join the trip
    url(r'^trips/cancel/(?P<trip_id>\d+)$', views.cancel_trip), # method 5.2 - cancel the trip

    url(r'^trips_edit_trip/(?P<trip_id>\d+)$', views.edit_trip_edit), # method 6 - edit trip information
    url(r'^trips/create_trip$', views.create_trip) # method 7 - create a new trip
]