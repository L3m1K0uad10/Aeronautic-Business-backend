import json

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Consultation



@csrf_exempt
def consultation_view(request, pk = None, *args, **kwargs):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('name')
            email = data.get('email')
            consultation_type = data.get('consultation_type')
            date = data.get('date')
            time = data.get('time')
            message = data.get('message', '')

            if not all([name, email, consultation_type, date, time]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            consultation = Consultation.objects.create(
                name=name,
                email=email,
                consultation_type=consultation_type,
                date=date,
                time=time,
                message=message
            )

            return JsonResponse({'message': 'Consultation request submitted successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    elif request.method == "GET":
        if pk:
            try:
                consultation = get_object_or_404(Consultation, pk=pk)
                data = {
                    'id': consultation.id,
                    'name': consultation.name,
                    'email': consultation.email,
                    'consultation_type': consultation.consultation_type,
                    'date': consultation.date,
                    'time': consultation.time,
                    'message': consultation.message,
                    'created_at': consultation.created_at,
                }
                return JsonResponse(data, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            try:
                consultations = Consultation.objects.all().order_by('-created_at')
                data = []
                for consultation in consultations:
                    data.append({
                        'id': consultation.id,
                        'name': consultation.name,
                        'email': consultation.email,
                        'consultation_type': consultation.consultation_type,
                        'date': consultation.date,
                        'time': consultation.time,
                        'message': consultation.message,
                        'created_at': consultation.created_at,
                    })
                return JsonResponse(data, status=200, safe=False)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
            
    elif request.method == "DELETE":
        if pk:
            try:
                consultation = get_object_or_404(Consultation, pk=pk)
                consultation.delete()
                return JsonResponse({'message': 'Consultation deleted successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Consultation ID is required for deletion'}, status=400)