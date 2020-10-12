from django.shortcuts import render
from django.http import HttpResponse
from .models import Platform

# Create your views here.
def index(request):
    platform = Platform.objects.using('labpostgres').all()
    
    return render(request,'iur/index.html',{'platform':platform})