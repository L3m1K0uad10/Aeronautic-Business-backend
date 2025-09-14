import json
import datetime
import re

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .models import Flight



# Custom function to parse ISO 8601 durations like P3H
def parse_duration_string(duration_str):
    if not isinstance(duration_str, str):
        raise ValueError("Duration must be a string.")
    
    # Regex to match formats like P<hours>H, P<minutes>M, or P<seconds>S
    match = re.match(r'^P(\d+)(H|M|S)$', duration_str.upper())
    
    if not match:
        raise ValueError("Invalid duration format. Use P<value>H, P<value>M, or P<value>S.")
    
    value = int(match.group(1))
    unit = match.group(2)
    
    if unit == 'H':
        return datetime.timedelta(hours=value)
    elif unit == 'M':
        return datetime.timedelta(minutes=value)
    elif unit == 'S':
        return datetime.timedelta(seconds=value)


@csrf_exempt 
def flight_view(request, pk = None, *args, **kwargs):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            flight_number = data.get("flight_number")
            departure = data.get("departure")
            arrival = data.get("arrival")
            departure_time = data.get("departure_time")
            arrival_time = data.get("arrival_time")
            price = data.get("price")
            airline = data.get("airline")
            duration = data.get("duration")
            seats_available = data.get("seats_available")

            # Convert the ISO 8601 duration string to a timedelta object
            try:
                duration = parse_duration_string(duration)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)

            if Flight.objects.filter(flight_number = flight_number).exists():
                return JsonResponse({"error": "Flight with this flight number already exists"})
            
            flight = Flight(
                flight_number = flight_number,
                departure = departure,
                arrival = arrival,
                departure_time = departure_time,
                arrival_time = arrival_time,
                price = price,
                airline = airline,
                duration = duration,
                seats_available = seats_available
            )
            flight.save()

            data = {
                "id": flight.id,
                "flight_number": flight.flight_number,
                "departure": flight.departure,
                "arrival": flight.arrival,
                "departure_time": flight.departure_time,
                "arrival_time": flight.arrival_time,
                "price": flight.price,
                "airline": flight.airline,
                "duration": duration,
                "seats_available": flight.seats_available
            }
            return JsonResponse(data, status = 201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status = 400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status = 500)
        
    elif request.method == "GET":
        if pk:
            try:
                flight = Flight.objects.get(id = pk)
                data = {
                    "id": flight.id,
                    "flight_number": flight.flight_number,
                    "departure": flight.departure,
                    "arrival": flight.arrival,
                    "departure_time": flight.departure_time,
                    "arrival_time": flight.arrival_time,
                    "price": flight.price,
                    "airline": flight.airline,
                    "duration": flight.duration,
                    "seats_available": flight.seats_available
                }
                return JsonResponse(data, status = 200)
            except Flight.DoesNotExist:
                return JsonResponse({"error": "Flight not found"}, status = 404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status = 500)
            
        else:
            try:
                flights = Flight.objects.all()
                data = []
                for flight in flights:
                    data.append({   
                        "id": flight.id,
                        "flight_number": flight.flight_number,
                        "departure": flight.departure,
                        "arrival": flight.arrival,
                        "departure_time": flight.departure_time,
                        "arrival_time": flight.arrival_time,
                        "price": flight.price,
                        "airline": flight.airline,
                        "duration": flight.duration,
                        "seats_available": flight.seats_available
                    })
                    
                return JsonResponse(data, safe = False, status = 200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status = 500)
    
    elif request.method == "PUT":
        if not pk:
            return JsonResponse({"error": "Method PUT not allowed"}, status = 400)
        try:
            data = json.loads(request.body.decode("utf-8"))

            flight = Flight.objects.get(id = pk)

            flight_number = data.get("flight_number")
            departure = data.get("departure")
            arrival = data.get("arrival")
            departure_time = data.get("departure_time")
            arrival_time = data.get("arrival_time")
            price = data.get("price")
            airline = data.get("airline")
            duration = data.get("duration")
            seats_available = data.get("seats_available")

            if flight_number:
                flight.flight_number = flight_number
            if departure:
                flight.departure = departure
            if arrival:
                flight.arrival = arrival
            if departure_time:
                flight.departure_time = departure_time
            if arrival_time:
                flight.arrival_time = arrival_time
            if price:
                flight.price = price
            if airline:
                flight.airline = airline
            if duration:
                try:
                    duration = parse_duration_string(duration)
                except ValueError as e:
                    return JsonResponse({"error": str(e)}, status=400)
                flight.duration = duration
            if seats_available:
                flight.seats_available = seats_available
            
            flight.save()

            data = {
                "id": flight.id,
                "flight_number": flight.flight_number,
                "departure": flight.departure,
                "arrival": flight.arrival,
                "departure_time": flight.departure_time,
                "arrival_time": flight.arrival_time,
                "price": flight.price,
                "airline": flight.airline,
                "duration": flight.duration,
                "seats_available": flight.seats_available
            }
            return JsonResponse(data, status = 200)
        except Flight.DoesNotExist:
            return JsonResponse({"error": "Flight not found"}, status = 404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status = 400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status = 500)
        
    elif request.method == "DELETE":
        if not pk:
            return JsonResponse({"error": "Method DELETE not allowed"}, status = 400)
        try:
            obj = get_object_or_404(Flight, id = pk)
            obj.delete()
            return JsonResponse({"message": "Flight deleted successfully"}, status = 204)
        except Flight.DoesNotExist:
            return JsonResponse({"error": "Flight not found"}, status = 404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status = 500)
    
    else:
        return JsonResponse({"error": "Method not allowed"}, status = 405)