from django.urls import path 

from .views import BookingListCreate, BookingDetail



# "bookings/ -> BookingListCreate (list, create)
# "bookings/<int:pk>/ -> BookingDetail (retrieve, update, delete)
urlpatterns = [
    path('bookings/', BookingListCreate.as_view(), name = 'booking_list_create'),
    path('bookings/<int:pk>/', BookingDetail.as_view(), name = 'booking_detail_update_delete'),
]