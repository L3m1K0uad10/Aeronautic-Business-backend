from django.urls import path 

from .views import consultation_view



# "consultation/ -> consultation_view (list, create)
# "consultation/<int:pk>/ -> consultation_view (retrieve, delete)
urlpatterns = [
    path('consultation/', consultation_view, name = 'consultation_list_create'),
    path('consultation/<int:pk>/', consultation_view, name = 'consultation_detail_delete'),
]