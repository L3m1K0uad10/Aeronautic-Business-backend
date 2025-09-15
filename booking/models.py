import uuid

from django.db import models
from django.conf import settings

from flights.models import Flight



class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    seat_number = models.CharField(max_length=10)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    reference_code = models.CharField(max_length=12, unique=True, editable=False)
    is_confirmed = models.BooleanField(default=False)  # only true after payment

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = str(uuid.uuid4().hex[:12]).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Booking {self.id} for {self.full_name} on {self.flight.flight_number}'


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    def __str__(self):
        return f"Payment {self.id} ({self.status})"