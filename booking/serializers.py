from rest_framework import serializers

from .models import Booking 
from flights.models import Flight
from flights.serializers import FlightSerializer



class BookingSerializer(serializers.ModelSerializer):
    # This field is used for writing (creating/updating)
    # The client sends a flight ID, and DRF automatically gets the Flight object
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all(), write_only=True)
    
    # This field is for reading (GET requests)
    # It will serialize the entire Flight object for the response
    flight_details = FlightSerializer(source='flight', read_only=True)
    
    class Meta:
        model = Booking 
        fields = '__all__'
        read_only_fields = ['id', 'booking_date', 'reference_code', 'is_confirmed', 'created_at']
    
    def validate(self, data):
        # DRF's PrimaryKeyRelatedField handles getting the Flight object
        flight = data.get('flight')
        seat_number = data.get('seat_number')

        if not flight:
            raise serializers.ValidationError("Flight is a required field.")

        # Checking for seat availability (one seat per booking)
        if flight.seats_available <= 0:
            raise serializers.ValidationError("No seats available on this flight.")
        
        # Checking if the seat is already taken on this flight
        if Booking.objects.filter(flight=flight, seat_number=seat_number).exists():
             raise serializers.ValidationError("This seat number is already taken for this flight.")
        
        return data 
    
    def create(self, validated_data):
        # decreasing seats_available on the flight
        flight = validated_data.get('flight')
        flight.seats_available -= 1
        flight.save()

        # creating the booking instance
        return super().create(validated_data)