from django.urls import path 

from .views import flight_list_create, flight_detail



# "flights/ -> flight_list_create (list, create)
# "flights/<int:pk>/ -> flight_detail (retrieve, update, delete)
urlpatterns = [
    path('flights/', flight_list_create, name='flight_list_create'),
    path('flights/<int:pk>/', flight_detail, name='flight_detail'),
]