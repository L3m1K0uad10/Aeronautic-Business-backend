from rest_framework import generics

from .models import Flight
from .serializers import FlightSerializer



class FlightListCreate(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    lookup_field = 'pk'