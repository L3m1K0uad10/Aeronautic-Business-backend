from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

from .models import Booking
from .serializers import BookingSerializer

class BookingListCreate(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # Custom business logic for sending an email
        subject = "Flight Booking Instructions"
        message = (
            f"Dear {booking.full_name},\n\n"
            f"Thank you for booking flight {booking.flight.flight_number}.\n"
            f"Your booking reference code is {booking.reference_code}.\n\n"
            "To confirm your booking, please proceed with the payment to our account.\n"
            "After payment, you will receive a confirmation email with your ticket details.\n\n"
            "bank: XYZ Bank\n"
            "account number: 123456789\n"
            "account name: Flight Booking Services\n\n"
            "Best regards,\n"
            "Flight Booking Team"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.email],
            fail_silently=False,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Custom business logic to re-increment seat availability
        instance.flight.seats_available += 1
        instance.flight.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)