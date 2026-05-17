# from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from django.http import JsonResponse

def test_api(request):
    return JsonResponse({
        "message": "Django fonctionne avec React "
    })