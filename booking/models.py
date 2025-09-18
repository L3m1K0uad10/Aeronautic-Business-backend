import uuid

from django.db import models
from flights.models import Flight



class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    seat_number = models.CharField(max_length=10)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    reference_code = models.CharField(max_length=12, unique=True, editable=False)
    is_confirmed = models.BooleanField(default=False)  # Manually set to True after payment confirmation

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = str(uuid.uuid4().hex[:12]).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Booking {self.reference_code} for {self.full_name} ({self.flight.flight_number})'
