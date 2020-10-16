from django.shortcuts import render
from django.http import HttpResponse
from .models import Platform,Uut

# Create your views here.
def index(request):
    # platform = Platform.objects.using('labpostgres').all()
    platform = Platform.objects.all()
    return render(request,'iur/index.html',{'platform':platform})

from django.contrib.auth.models import User,Group
from rest_framework import viewsets,permissions
from .serializers import UserSerializer,GroupSerializer,UutSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_class = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_class = [permissions.IsAuthenticated]

class UutViewSet(viewsets.ModelViewSet):
    queryset = Uut.objects.order_by('-id')
    serializer_class = UutSerializer
    permission_class = [permissions.IsAuthenticated]

