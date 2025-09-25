import uuid

from django.db import models
from flights.models import Flight, FlightClassDetail



# Create your models here.
class Booking(models.Model):
    """
    Represents a flight booking made by a customer.
    """
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )

    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name='bookings'
    )
    # This ForeignKey has been updated to point to the correct model
    flight_class = models.ForeignKey(
        FlightClassDetail, on_delete=models.CASCADE, related_name='bookings'
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    seat_number = models.CharField(max_length=10, blank=True, null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending'
    )
    # Added reference_code for email confirmation
    reference_code = models.CharField(max_length=10, unique=True, blank=True)

    class Meta:
        verbose_name = "Flight Booking"
        verbose_name_plural = "Flight Bookings"
        ordering = ['-booking_date']

    def __str__(self):
        return f"Booking for {self.full_name} on Flight {self.flight.flight_number}"

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a unique reference code.
        """
        if not self.reference_code:
            self.reference_code = str(uuid.uuid4().hex[:10]).upper()
        super().save(*args, **kwargs)
