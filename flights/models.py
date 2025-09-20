# flights/models.py
from django.db import models



class Flight(models.Model):
    FLIGHT_CLASSES = [
        ('economy', 'Economy'),
        ('premium_economy', 'Premium Economy'),
        ('business', 'Business'),
        ('first', 'First Class'),
    ]

    flight_number = models.CharField(max_length=10)
    # Using CharFields to simplify things
    departure_airport_name = models.CharField(max_length=255)
    arrival_airport_name = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    airline = models.CharField(max_length=100)
    duration = models.DurationField()
    seats_available = models.IntegerField()
    flight_class = models.CharField(max_length=50, choices=FLIGHT_CLASSES, default='economy')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.flight_number} - {self.departure_airport_name} to {self.arrival_airport_name}"