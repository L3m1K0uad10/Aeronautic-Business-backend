# flights/filters.py

import django_filters
from .models import Flight
from datetime import datetime, timedelta



class FlightFilter(django_filters.FilterSet):
    # Filter for flights departing on a specific date.
    departure_date = django_filters.DateFilter(field_name='departure_time', lookup_expr='date')
    
    # Filter for flights returning on or after a specific date.
    # The user can enter this date, but it's not mandatory.
    return_date = django_filters.DateFilter(field_name='arrival_time', lookup_expr='date__gte')

    # Filter for the number of passengers, ensuring seats are available.
    passengers = django_filters.NumberFilter(field_name='seats_available', lookup_expr='gte')
    
    # Filter by travel class.
    flight_class = django_filters.CharFilter(field_name='flight_class')
    
    # Filter by departure and arrival airports.
    departure_airport = django_filters.CharFilter(field_name='departure_airport_name', lookup_expr='icontains')
    arrival_airport = django_filters.CharFilter(field_name='arrival_airport_name', lookup_expr='icontains')

    class Meta:
        model = Flight
        fields = ['departure_date', 'return_date', 'passengers', 'flight_class', 'departure_airport', 'arrival_airport']