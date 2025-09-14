from django.db import models



class Flight(models.Model):
    flight_number = models.CharField(max_length = 10)
    departure = models.CharField(max_length = 100)
    arrival = models.CharField(max_length = 100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    airline = models.CharField(max_length = 100)
    duration = models.DurationField()
    seats_available = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.flight_number} - {self.departure} to {self.arrival}"


""" class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete = models.CASCADE)
    passenger_name = models.CharField(max_length = 100)
    passenger_email = models.EmailField()
    booking_date = models.DateTimeField(auto_now_add = True)
    seat_number = models.CharField(max_length = 10)
    status = models.CharField(max_length = 20, choices = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending')
    ]) 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"Booking for {self.passenger_name} on flight {self.flight.flight_number}" """

