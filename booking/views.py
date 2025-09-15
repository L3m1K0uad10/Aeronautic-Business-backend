import json
import re
import uuid
import requests

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from flights.models import Flight
from .models import Booking, Payment


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

            # Validate email format
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                return JsonResponse({'error': 'Invalid email format'}, status=400)

            # Validate phone number format (E.164)
            phone_regex = r'^\+?[1-9]\d{1,14}$'
            if not re.match(phone_regex, phone_number):
                return JsonResponse({'error': 'Invalid phone number format'}, status=400)

            # Lookup flight
            flight = get_object_or_404(Flight, id=flight_id)

            # Create pending booking
            booking = Booking.objects.create(
                flight=flight,
                seat_number=seat_number,
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                is_confirmed=False,  # will be set True after payment
            )

            return JsonResponse({
                'message': 'Booking created. Please proceed to payment.',
                'booking_id': booking.id,
                'reference_code': booking.reference_code
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET' and pk is not None:
        try:
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
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method or missing booking ID'}, status=400)


@csrf_exempt
def create_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            booking_id = data.get("booking_id")
            amount = data.get("amount")  # in USD
            currency = data.get("currency", "USD")

            booking = get_object_or_404(Booking, id=booking_id)

            # Generate unique transaction reference
            tx_ref = f"booking_{booking.id}_{uuid.uuid4().hex[:8]}"

            # Call Flutterwave API
            url = "https://api.flutterwave.com/v3/payments"
            headers = {
                "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "tx_ref": tx_ref,
                "amount": str(amount),
                "currency": currency,
                "redirect_url": settings.FLW_REDIRECT_URL,  # must be registered in Flutterwave dashboard
                "customer": {
                    "email": booking.email,
                    "name": booking.full_name,
                    "phonenumber": booking.phone_number,
                },
                "customizations": {
                    "title": "Flight Booking",
                    "description": f"Payment for booking {booking.id}",
                },
            }

            response = requests.post(url, json=payload, headers=headers).json()

            if response.get("status") != "success":
                return JsonResponse({"error": "Failed to initialize payment"}, status=400)

            # Save payment locally
            payment = Payment.objects.create(
                booking=booking,
                amount=amount,
                currency=currency,
                payment_method="flutterwave",
                transaction_id=tx_ref,
                status="pending",
            )

            return JsonResponse(
                {"payment_link": response["data"]["link"], "payment_id": payment.id},
                status=201,
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def verify_payment(request):
    """Redirect URL called by Flutterwave after payment"""
    tx_ref = request.GET.get("tx_ref")
    status = request.GET.get("status")

    payment = Payment.objects.filter(transaction_id=tx_ref).first()
    if not payment:
        return JsonResponse({"error": "Payment not found"}, status=404)

    if status == "successful":
        payment.status = "success"
        payment.save()
        booking = payment.booking
        booking.is_confirmed = True
        booking.save()
        return JsonResponse({"message": "Payment successful, booking confirmed!"})

    else:
        payment.status = "failed"
        payment.save()
        return JsonResponse({"message": "Payment failed"})


@csrf_exempt
def flutterwave_webhook(request):
    """Webhook called by Flutterwave for payment events"""
    try:
        payload = json.loads(request.body)
        tx_ref = payload["data"]["tx_ref"]
        status = payload["data"]["status"]

        payment = Payment.objects.filter(transaction_id=tx_ref).first()
        if payment:
            if status == "successful":
                payment.status = "success"
                payment.booking.is_confirmed = True
                payment.booking.save()
            else:
                payment.status = "failed"
            payment.save()

        return HttpResponse(status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
