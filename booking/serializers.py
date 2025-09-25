from rest_framework import serializers

from .models import Booking
from flights.models import Flight, FlightClassDetail



class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    """
    # Use a CharField to accept the flight_class name from the frontend
    flight_class_name = serializers.CharField(write_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'flight',
            'flight_class_name',
            'full_name',
            'email',
            'phone_number',
            'seat_number',
            'booking_date',
            'status',
            'reference_code'
        ]
        read_only_fields = ['booking_date', 'status', 'reference_code']

    def validate(self, data):
        """
        Custom validation to check for flight and seat availability.
        """
        flight = data.get('flight')
        flight_class_name = data.get('flight_class_name')
        
        if not all([flight, flight_class_name]):
            raise serializers.ValidationError(
                "Flight and flight class must be provided."
            )
        
        try:
            # Get the specific FlightClassDetail instance
            flight_class_obj = FlightClassDetail.objects.get(
                flight=flight, flight_class=flight_class_name
            )
        except FlightClassDetail.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid flight class for the selected flight."
            )
        
        if flight_class_obj.seats_available <= 0:
            raise serializers.ValidationError(
                "No seats available for this flight class."
            )
        
        # Add the validated FlightClassDetail object to the data for the create method
        data['flight_class'] = flight_class_obj
        return data

    def create(self, validated_data):
        """
        Creates a new booking and updates the available seats.
        """
        # Remove the temporary 'flight_class_name' field
        validated_data.pop('flight_class_name')

        booking = Booking.objects.create(**validated_data)
        
        # Decrement the seats available for the booked flight class
        booking.flight_class.seats_available -= 1
        booking.flight_class.save()

        return booking
