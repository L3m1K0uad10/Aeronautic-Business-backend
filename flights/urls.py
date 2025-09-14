from django.urls import path 

from .views import flight_view



# "flights/ -> flight_view (list, create)
# "flights/<int:pk>/ -> flight_view (retrieve, update, delete)
urlpatterns = [
    path('flights/', flight_view, name = 'flight_list_create'),
    path('flights/<int:pk>/', flight_view, name = 'flight_detail_update_delete'),
]