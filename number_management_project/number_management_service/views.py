import json
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def fetch_numbers(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("numbers", [])
    return []

@require_GET
def get_numbers(request):
    urls = request.GET.getlist("url")
    results = []

    for url in urls:
        numbers = fetch_numbers(url)
        results.append(numbers)

    merged_numbers = sorted(set(number for sublist in results for number in sublist))
    response_data = {"numbers": merged_numbers}
    return JsonResponse(response_data, safe=False)
