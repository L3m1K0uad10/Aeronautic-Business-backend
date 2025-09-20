from django.urls import path 

from .views import consultation_list_create, consultation_detail



# "consultations/ -> consultation_list_create (list, create)
# "consultations/<int:pk>/ -> consultation_detail (retrieve, delete)
urlpatterns = [
    path('consultations/', consultation_list_create, name = 'consultation_list_create'),
    path('consultations/<int:pk>/', consultation_detail, name = 'consultation_detail_delete'),
]