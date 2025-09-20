from django.urls import path 

from .views import FlightListCreate, FlightDetail



# "flights/ -> FlightListCreate (list, create)
# "flights/<int:pk>/ -> FlightDetail (retrieve, update, delete)
urlpatterns = [
    path('flights/', FlightListCreate.as_view(), name='flight_list_create'),
    path('flights/<int:pk>/', FlightDetail.as_view(), name='flight_detail'),
]