from django.urls import path 

from .views import booking_view



# "booking/ -> booking_view (list, create)
# "booking/<int:pk>/ -> booking_view (retrieve, update, delete)
urlpatterns = [
    path('booking/', booking_view, name = 'booking_list_create'),
    path('booking/<int:pk>/', booking_view, name = 'booking_detail_update_delete'),
]