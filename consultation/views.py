from rest_framework import generics

from .models import Consultation
from .serializers import ConsultationSerializer



class ConsultationListCreate(generics.ListCreateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer


class ConsultationDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    lookup_field = 'pk'