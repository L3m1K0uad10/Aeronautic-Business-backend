import json
import re

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

from flights.models import Flight
from .models import Booking



def validate_email_format(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_phone_format(phone):
    phone_regex = r'^\+?[1-9]\d{1,14}$'
    return re.match(phone_regex, phone) is not None


@csrf_exempt
def booking_view(request, pk=None, *args, **kwargs):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            flight_id = data.get('flight')
            seat_number = data.get('seat_number')
            email = data.get('email')
            phone_number = data.get('phone_number')
            full_name = data.get('full_name')

            if not all([full_name, email, phone_number, seat_number, flight_id]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            if validate_email_format(email) is False:
                return JsonResponse({'error': 'Invalid email format'}, status=400)

            if validate_phone_format(phone_number) is False:
                return JsonResponse({'error': 'Invalid phone number format'}, status=400)

            # Lookup flight
            flight = get_object_or_404(Flight, id = flight_id)

            # Create pending booking
            booking = Booking.objects.create(
                flight=flight,
                seat_number=seat_number,
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                is_confirmed=False,
            )

            # Send email with manual payment instructions
            subject = "Flight Booking Instructions"
            message = (
                f"Dear {full_name},\n\n"
                f"Thank you for booking flight {flight.flight_number}.\n"
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
                [email],
                fail_silently=False,
            )

            return JsonResponse({
                'message': 'Booking created. Instructions sent to email.',
                'booking_id': booking.id,
                'reference_code': booking.reference_code
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET':
        try:
            if pk is not None:
                booking = get_object_or_404(Booking, pk=pk)
                booking_data = {
                    'id': booking.id,
                    'flight_id': booking.flight.id,
                    'full_name': booking.full_name,
                    'email': booking.email,
                    'phone_number': booking.phone_number,
                    'seat_number': booking.seat_number,
                    'booking_date': booking.booking_date.isoformat(),
                    'is_confirmed': booking.is_confirmed,
                    'reference_code': booking.reference_code,
                }
                return JsonResponse(booking_data, status=200)

            else:
                bookings = Booking.objects.all().order_by('-booking_date')
                booking_list = []
                for booking in bookings:
                    booking_list.append({
                        'id': booking.id,
                        'flight_id': booking.flight.id,
                        'full_name': booking.full_name,
                        'email': booking.email,
                        'phone_number': booking.phone_number,
                        'seat_number': booking.seat_number,
                        'booking_date': booking.booking_date.isoformat(),
                        'is_confirmed': booking.is_confirmed,
                        'reference_code': booking.reference_code,
                    })
                return JsonResponse({'bookings': booking_list}, status=200, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
     
    elif request.method == 'PUT' and pk is not None:
        try:
            data = json.loads(request.body)
            booking = get_object_or_404(Booking, pk=pk)

            booking.full_name = data.get('full_name', booking.full_name)
            booking.email = data.get('email', booking.email)
            booking.phone_number = data.get('phone_number', booking.phone_number)
            booking.seat_number = data.get('seat_number', booking.seat_number)
            booking.is_confirmed = data.get('is_confirmed', booking.is_confirmed)

            if 'flight' in data:
                flight = get_object_or_404(Flight, id=data['flight'])
                booking.flight = flight

            booking.save()

            return JsonResponse({'message': 'Booking updated successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE' and pk is not None:
        try:
            booking = get_object_or_404(Booking, pk=pk)
            booking.delete()
            return JsonResponse({'message': 'Booking deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method or missing booking ID'}, status=400)
