from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Consultation
from .serializers import ConsultationSerializer



@api_view(['GET', 'POST'])
def consultation_list_create(request):
    """
    List all consultations or create a new consultation.
    """
    if request.method == 'GET':
        consultations = Consultation.objects.all()
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def consultation_detail(request, pk):
    """
    Retrieve or delete a consultation instance.
    """
    consultation = get_object_or_404(Consultation, pk=pk)

    if request.method == 'GET':
        serializer = ConsultationSerializer(consultation)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        consultation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)