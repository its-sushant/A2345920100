from datetime import datetime, timedelta
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Train

@api_view(['GET'])
def get_trains(request):
    # Get data from John Doe Railway API
    response = requests.get('http://20.244.56.144/train/trains', headers={
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTIzNjg4NzIsImNvbXBhbnlOYW1lIjoiVHJhaW4gQ2VudHJhbCIsImNsaWVudElEIjoiNTc2YzM4NDctOTc1YS00YzE2LWIxZjEtMGZjMTI4OTA3MzhhIiwib3duZXJOYW1lIjoiIiwib3duZXJFbWFpbCI6IiIsInJvbGxObyI6IkNTRS1BMjM0NTkyMDEwMCJ9.4by5EuadlF3JfWM0uib5ccsmHSxC4wQBtoWDMr1y50M'
    })
    trains_data = response.json()

    # Process the data and create Train objects
    trains = []
    now = datetime.now()
    for train_data in trains_data:
        departure_time = now + timedelta(hours=train_data['departureTime']['Hours'], minutes=train_data['departureTime']['Minutes'])
        train = Train(
            train_name=train_data['trainName'],
            train_number=train_data['trainNumber'],
            departure_time=departure_time,
            sleeper_available=train_data['seatsAvailable']['sleeper'],
            ac_available=train_data['seatsAvailable']['AC'],
            sleeper_price=train_data['price']['sleeper'],
            ac_price=train_data['price']['AC'],
            delayed_by=train_data['delayedBy']
        )
        trains.append(train)

    # Sort the trains based on your criteria
    sorted_trains = sorted(trains, key=lambda t: (t.sleeper_price, -t.sleeper_available, t.departure_time), reverse=True)

    # Serialize the sorted trains and return the response
    serialized_trains = [{'train_name': t.train_name, 'train_number': t.train_number,
                          'departure_time': t.departure_time.strftime('%H:%M:%S'),
                          'sleeper_available': t.sleeper_available, 'ac_available': t.ac_available,
                          'sleeper_price': t.sleeper_price, 'ac_price': t.ac_price,
                          'delayed_by': t.delayed_by} for t in sorted_trains]

    return JsonResponse(serialized_trains, safe=False)
