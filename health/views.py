from django.shortcuts import render
from django.http import HttpResponse

def health_check(request):
    return HttpResponse()
