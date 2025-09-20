from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Flight
from .serializers import FlightSerializer
from .filters import FlightFilter



class FlightListCreate(generics.ListCreateAPIView):
    queryset = Flight.objects.all().prefetch_related('class_details')
    serializer_class = FlightSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightFilter


class FlightDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all().prefetch_related('class_details')
    serializer_class = FlightSerializer
    lookup_field = 'pk'
