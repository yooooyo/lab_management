# from django.shortcuts import render,get_list_or_404,get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets,permissions
from iur.serializers import Uut,UutSerializer,Member,MemberSerializer
from .serializers import TaskSerializer,Task,ScriptSerializer,Script,ApSerializer,Ap,TaskStatusSerializer,TaskStatus
from django.db.models import Q 
from rest_framework import status
import uuid

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_class = [permissions.IsAuthenticated,permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        task_group = self.request.query_params.get('task_group',None)
        if task_group:
            queryset = queryset.filter(task_group=task_group)
        return queryset
    
    def format_post_request(self,request:Request):
        data ={}
        uut = request.data.get('sn',None)
        # uut = UutSerializer(Uut.objects.get(sn__iexact=uut)) if uut else uut
        uut = Uut.objects.get(sn__iexact=uut) if uut else uut
        uut_uuid = request.data.get('uut_uuid',None)
        uut_uuid = str(uuid.uuid4()) if not uut and not uut_uuid else uut_uuid

        if uut:data.update({'uut':uut.id}) 
        else: data.update({'uut_uuid':uut_uuid})

        uut_info = request.data.get('uut_info',None)
        script = request.data.get('script',None)
        # script = ScriptSerializer(Script.objects.get(name__iexact=script))
        script = Script.objects.get(name__iexact=script)
        # status = TaskStatusSerializer(TaskStatus.objects.get(status_text__iexact='wait'))
        status = TaskStatus.objects.get(status_text__iexact='wait')
        ap = request.data.get('ssid',None)
        if ap:
            ap =  Ap.objects.get(Q(ssid_2d4__iexact=ap)|Q(ssid_5__iexact=ap))
        else:
            ap = Ap.objects.get(is_default=True)
        # ap = ApSerializer(ap)
        task_group = request.data.get('task_group',None)
        task_group = Task.objects.filter(task_group__iexact=task_group) if task_group else task_group
        group_series=0
        if task_group:
            group_series = task_group.order_by('-group_series').first().group_series + 1
            task_group = task_group.first().task_group
        else:
            task_group = str(uuid.uuid4())

        data.update({
            'script':script.id,
            'status':status.id,
            'ap':ap.id,
            'uut_info':uut_info,
            'task_group':task_group,
            'group_series':group_series
        })
        return data
    
    def perform_create(self, serializer):
        serializer.save(assigner=self.request.user)

    def create(self, request:Request, *args, **kwargs):
        data = self.format_post_request(request)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        return super().perform_update(serializer)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)



    

class ScriptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer
    permission_class = [permissions.IsAuthenticated,permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name',None)
        if name:
            queryset = queryset.filter(name__iexact=name)
        return queryset

class ApViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ap.objects.all()
    serializer_class = ApSerializer
    permission_class = [permissions.IsAuthenticated,permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        ssid = self.request.query_params.get('ssid',None)
        if ssid:
            queryset = queryset.filter(ssid_2d4__iexact=ssid) | queryset.filter(ssid_5__iexact=ssid)
        return queryset

class TaskStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    permission_class = [permissions.IsAuthenticated,permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status',None)
        if status:
            queryset = queryset.filter(status_text__iexact=status)
        return queryset


