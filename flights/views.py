# flights/views.py

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Flight
from .serializers import FlightSerializer
from .filters import FlightFilter  # Import the filter class



class FlightListCreate(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    
    # Add these lines to enable filtering
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightFilter


class FlightDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    lookup_field = 'pk'