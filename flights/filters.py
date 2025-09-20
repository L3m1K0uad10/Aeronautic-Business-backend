import django_filters
from django.db.models import Q

from .models import Flight



class FlightFilter(django_filters.FilterSet):
    departure_date = django_filters.DateFilter(field_name='departure_time', lookup_expr='date')
    return_date = django_filters.DateFilter(field_name='arrival_time', lookup_expr='date__gte')
    passengers = django_filters.NumberFilter(method='filter_by_class_and_passengers')
    departure_airport = django_filters.CharFilter(field_name='departure_airport_name', lookup_expr='icontains')
    arrival_airport = django_filters.CharFilter(field_name='arrival_airport_name', lookup_expr='icontains')
    flight_class = django_filters.CharFilter(field_name='class_details__flight_class')


    def filter_by_class_and_passengers(self, queryset, name, value):
        flight_class = self.request.GET.get('flight_class', None)
        
        # If no flight class is specified, we check for available seats in ANY class
        if not flight_class:
            return queryset.filter(class_details__seats_available__gte=value).distinct()
        
        # Otherwise, filter by both the specified class and number of passengers.
        return queryset.filter(
            class_details__flight_class=flight_class,
            class_details__seats_available__gte=value
        ).distinct()


    class Meta:
        model = Flight
        fields = ['departure_date', 'return_date', 'passengers', 'flight_class', 'departure_airport', 'arrival_airport']
