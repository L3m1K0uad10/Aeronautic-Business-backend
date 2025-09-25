import os

from rest_framework import generics, status
from rest_framework.response import Response

from .models import Consultation
from .serializers import ConsultationSerializer



class ConsultationListCreate(generics.ListCreateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

    def create(self, request, *args, **kwargs):
        # 1. Validate and Save the Consultation Data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # 2. Prepare and Send Response
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Consultation successfully booked."}, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )


class ConsultationDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    lookup_field = 'pk'