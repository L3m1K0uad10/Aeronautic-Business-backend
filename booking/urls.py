from django.urls import path 

from .views import booking_list_create, booking_detail



# "bookings/ -> booking_list_create (list, create)
# "bookings/<int:pk>/ -> booking_detail (retrieve, update, delete)
urlpatterns = [
    path('bookings/', booking_list_create, name = 'booking_list_create'),
    path('bookings/<int:pk>/', booking_detail, name = 'booking_detail_update_delete'),
]