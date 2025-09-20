from django.urls import path 

from .views import ConsultationListCreate, ConsultationDetailDelete



# "consultations/ -> ConsultationListCreate (list, create)
# "consultations/<int:pk>/ -> ConsultationDetailDelete (retrieve, delete)
urlpatterns = [
    path('consultations/', ConsultationListCreate.as_view(), name = 'consultation_list_create'),
    path('consultations/<int:pk>/', ConsultationDetailDelete.as_view(), name = 'consultation_detail_delete'),
]