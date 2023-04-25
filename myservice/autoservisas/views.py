from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def autoservice(request):
    return HttpResponse("Mano autoservisas")