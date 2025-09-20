from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

from .models import Booking
from .serializers import BookingSerializer



@api_view(['GET', 'POST'])
def booking_list_create(request):
    """
    List all bookings or create a new booking.
    """
    if request.method == 'GET':
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            
            # Email sending logic moved here from the serializer
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
            
            # The serializer.data now includes the flight_details field for a complete response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def booking_detail(request, pk):
    """
    Retrieve, update or delete a booking instance.
    """
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'GET':
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Re-increment the seats_available on the flight
        # This is a good practice to "return" the seat
        booking.flight.seats_available += 1
        booking.flight.save()
        
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)