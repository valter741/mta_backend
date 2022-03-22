from django.core import serializers
from django.shortcuts import render

from django.http import JsonResponse
from .models import User

def index(request):
    data = list(User.objects.values())

    return JsonResponse(data, safe=False)
