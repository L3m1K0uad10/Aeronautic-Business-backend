from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Flight
from .serializers import FlightSerializer



@api_view(['GET', 'POST'])
def flight_list_create(request):
    """
    List all flights or create a new flight.
    """
    if request.method == 'GET':
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def flight_detail(request, pk):
    """
    Retrieve, update or delete a flight instance.
    """
    flight = get_object_or_404(Flight, pk=pk)

    if request.method == 'GET':
        serializer = FlightSerializer(flight)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # The 'data' argument is the new data from the request
        # The 'instance' argument is the existing object to update
        serializer = FlightSerializer(flight, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)