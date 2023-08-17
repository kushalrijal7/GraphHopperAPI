import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests
import polyline
from datetime import datetime

@api_view(['POST'])
def get_route(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        coordinates = data.get('coordinates', [])
        routing_method = data.get('routingMethod', 'car')  # Default to car if not provided

        if len(coordinates) < 2:
            return JsonResponse({'error': 'At least two coordinates are required.'}, status=400)

        graphhopper_url = 'https://graphhopper.com/api/1/route'
        waypoints = [f"{coord['lat']},{coord['lng']}" for coord in coordinates]
        
        
        params = {
            'point': waypoints,
            'vehicle': routing_method,
            'key': '9ff239b1-8614-46af-8618-f6cb70310d18',
            'weighting': 'fastest',
        }
        
        response = requests.get(graphhopper_url, params=params)

        if response.status_code == 200:
            routing_data = response.json()
            
            encoded_polyline = routing_data['paths'][0]['points']
            distance = routing_data['paths'][0]['distance']
            time = routing_data['paths'][0]['time']
            
            route = {
                'encodedPolyline': encoded_polyline,
                'distanceInMeters': distance,
                'timeInMs': time,
                'instructionList': None  # You can add instructions here if available
            }
            
            #routes.append(route)
        else:
            return JsonResponse({'error': 'Error connecting to GraphHopper API.'}, status=500)
        # Generate a real timestamp
        timestamp = datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")
        
        status = 200
        message = "Success"
        
        response_data = {
            'timestamp': timestamp,
            'status': status,
            'message': message,
            'data': [route]
        }
        
        return JsonResponse(response_data)
    else:

        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)