from rest_framework import serializers

from .models import Flight 


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight 
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def validate_seats_available(self, value):
        if value < 0:
            raise serializers.ValidationError("Seats available cannot be negative.")
        return value
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
    
    def validate(self, data):
        # The 'data' dictionary may contain datetime objects
        departure_time = data.get('departure_time')
        arrival_time = data.get('arrival_time')
        
        # Ensuring both fields exist before comparison
        if departure_time and arrival_time and departure_time >= arrival_time:
            raise serializers.ValidationError("Departure time must be before arrival time.")
        return data
    