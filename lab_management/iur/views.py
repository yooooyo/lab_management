from django.shortcuts import render
from django.http import HttpResponse
from .models import Platform,Uut,PlatformConfig,UutPhase,UutStatus,PlatformPhase
from rest_framework.permissions import AllowAny

# Create your views here.
def index(request):
    # platform = Platform.objects.using('labpostgres').all()
    platform = Platform.objects.all()
    return render(request,'iur/index.html',{'platform':platform})

from django.contrib.auth.models import User,Group
from rest_framework import viewsets,permissions
from .serializers import UserSerializer,GroupSerializer,UutSerializer,PlatformConfigSerializer,\
        UutPhaseSerializer, \
        PlatformSerializer, \
        UutStatusSerializer, \
        PlatformPhaseSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_class = [AllowAny]

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_class = [AllowAny]

class UutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Uut.objects.order_by('-keyin_time')
    serializer_class = UutSerializer
    permission_class = [AllowAny]

    def get_queryset(self):
        queryset = Uut.objects.all()
        sn = self.request.query_params.get('sn', None)
        if sn :
            queryset = queryset.filter(sn__icontains=sn)
        return queryset


class PlatformConfigViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlatformConfig.objects.all()
    serializer_class = PlatformConfigSerializer
    permission_class = [AllowAny]

class UutPhaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UutPhase.objects.all()
    serializer_class = UutPhaseSerializer
    permission_class = [AllowAny]

class PlatformViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_class = [AllowAny]

class UutStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UutStatus.objects.all()
    serializer_class = UutStatusSerializer
    permission_class = [AllowAny]

class PlatformPhaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlatformPhase.objects.all()
    serializer_class = PlatformPhaseSerializer
    permission_class = [AllowAny]


