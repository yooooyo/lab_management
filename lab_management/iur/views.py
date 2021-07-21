from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Platform,Uut,PlatformConfig,UutPhase,UutStatus,PlatformPhase,Member
from rest_framework.permissions import AllowAny

# Create your views here.
def index(request):
    # platform = Platform.objects.using('labpostgres').all()
    platform = Platform.objects.all()
    return render(request,'iur/index.html',{'platform':platform})

from django.contrib.auth.models import User,Group
from rest_framework import viewsets,permissions
from .serializers import MemberSerializer, UserSerializer,GroupSerializer,UutSerializer,PlatformConfigSerializer,\
        UutPhaseSerializer, \
        PlatformSerializer, \
        UutStatusSerializer, \
        PlatformPhaseSerializer

class MemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Member.objects.all().order_by('usernameincompany')
    serializer_class = MemberSerializer
    permission_classes=[AllowAny]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_class = [AllowAny]

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_class = [AllowAny]

class UutViewSet(viewsets.ModelViewSet):
    queryset = Uut.objects.order_by('-keyin_time')
    serializer_class = UutSerializer
    permission_class = [AllowAny]

    def list(self, request:Request, *args, **kwargs):
        queryset = self.get_queryset()

        #quick get params
        sn = request.query_params.get('sn',None)
        if sn:
            queryset = queryset.filter(sn__icontains=sn)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


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


