from rest_framework import serializers
from .models import Flight, FlightClassDetail


class FlightClassDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightClassDetail
        fields = ['flight_class', 'price', 'seats_available']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_seats_available(self, value):
        if value < 0:
            raise serializers.ValidationError("Seats available cannot be negative.")
        return value
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value


class FlightSerializer(serializers.ModelSerializer):
    # This field is no longer read-only, so it can be used for POST requests.
    # The 'many=True' indicates it's a list of FlightClassDetail objects.
    class_details = FlightClassDetailSerializer(many=True)

    class Meta:
        model = Flight
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        departure_time = data.get('departure_time')
        arrival_time = data.get('arrival_time')
        
        if departure_time and arrival_time and departure_time >= arrival_time:
            raise serializers.ValidationError("Departure time must be before arrival time.")
        return data

    def create(self, validated_data):
        # Extract the list of class details from the validated data.
        class_details_data = validated_data.pop('class_details')
        
        # Create the main Flight instance first.
        flight = Flight.objects.create(**validated_data)
        
        # Loop through the class details data and create an instance for each entry,
        # linking it to the newly created flight.
        for detail_data in class_details_data:
            FlightClassDetail.objects.create(flight=flight, **detail_data)
            
        return flight
