# from django.shortcuts import render,get_list_or_404,get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers, viewsets,permissions
from iur.serializers import Uut,UutSerializer,Member,MemberSerializer
from .serializers import TaskIssueSerializer,TaskIssue, TaskSerializer,Task,ScriptSerializer,Script,ApSerializer,Ap,TaskStatusSerializer,TaskStatus,PowerState,PowerStateSerializer,GeneralQueryString,GeneralQueryStringSerializer
from django.db.models import Q, query 
from rest_framework import status
import uuid

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_class = [permissions.IsAuthenticated,permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        task_group = self.request.query_params.get('task_group',None)
        task_id = self.request.query_params.get('task_id',None)
        sn = self.request.query_params.get('sn',None)
        uut_uuid = self.request.query_params.get('uut_uuid',None)
        task = self.request.query_params.get('task',None)
        if task and sn:
            if task == 'current':
                queryset = queryset.filter(Q(uut__sn__icontains=sn) & Q(status__status_text__iexact='run'))
            elif task == 'previous':
                queryset = queryset.filter(uut_uuid=uut_uuid) # not yet
            elif task == 'next':
                queryset = queryset.filter(uut_uuid=uut_uuid) # not yet
            return queryset
        if task_group:
            queryset = queryset.filter(task_group=task_group)
        if task_id:
            queryset = queryset.filter(id=task_id)
        if sn:
            queryset = queryset.filter(uut__sn__icontains=sn)
        if uut_uuid:
            queryset = queryset.filter(uut_uuid=uut_uuid)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def format_post_request(self,request:Request):
        data ={}
        uut = request.data.get('sn',None)
        uut = Uut.objects.get(sn__icontains=uut) if uut else uut
        uut_uuid = request.data.get('uut_uuid',None)
        uut_uuid = str(uuid.uuid4()) if not uut and not uut_uuid else uut_uuid

        if uut:data.update({'uut':uut.id}) 
        else: data.update({'uut_uuid':uut_uuid})

        uut_info = request.data.get('uut_info',None)
        script = request.data.get('script',None)
        script = Script.objects.get(name__iexact=script)

        ap = request.data.get('ssid',None)
        if ap:
            ap =  Ap.find_or_create_by_ssid(ap)[0]
        else:
            ap = Ap.objects.get(is_default=True)

        # add by group_uuid or group_name
        group_uuid = request.data.get('group_uuid',None)
        group_name = request.data.get('group_name',None)
        # priority select
        tasks = None
        tasks_by_group = None
        if uut: tasks = Task.objects.filter(uut=uut)
        elif uut_uuid: tasks = Task.objects.filter(uut_uuid = uut_uuid)

        if group_name:
            pre_tasks = tasks.filter(group_name=group_name) 
            if pre_tasks.count()>0: tasks_by_group = pre_tasks
        elif group_uuid:
            pre_tasks = tasks.filter(group_uuid=group_uuid)
            if pre_tasks.count()>0: tasks_by_group = pre_tasks
            
        # already filter tasks by group name or group uuid, indentify task series in task group
        group_task_series = 0
        group_series = None
        if tasks_by_group:
            task = tasks_by_group.order_by('-group_task_series').first()
            group_task_series = task.group_task_series + 1
            group_uuid = task.group_uuid
            group_series = task.group_series
        else:
            group_uuid = str(uuid.uuid4())
            group_series = tasks.values_list("group_series",flat=True)
            group_series = max(group_series)+1 if group_series else 0

        task_status = request.data.get('status',None)
        if task_status:
            task_status = TaskStatus.objects.get(status_text__iexact=task_status)

        start_time = request.data.get('start_time',None)

        data.update({
            'script':script.id,
            'status':task_status.id,
            'ap':ap.id,
            'uut_info':uut_info,
            'group_uuid':group_uuid,
            'group_series':group_series,
            'group_name':group_name,
            'group_task_series':group_task_series,
            'start_time':start_time
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

    def format_put_request(self,request:Request):
        data = request.data.copy()
        script = data.get('script',None)
        if script:
            script = Script.objects.get(name__iexact=script) if script else script
            data.update({'script':script.id})
        ssid = request.data.get('ssid',None)
        ap = Ap.find_by_ssid(ssid)
        if ap:
            data.update({'ap':ap.id})
        task_status = request.data.get('status',None)
        if task_status:
            task_status = TaskStatus.objects.get(status_text__iexact = task_status)
            data.update({'status':task_status.id})
        group_uuid = data.get('group_uuid',None)
        group_name = data.get('group_name',None)

        tasks = None
        if group_uuid:
            tasks = Task.objects.filter(group_uuid = group_uuid).order_by('-group_task_series')
        if group_name:
            tasks = Task.objects.filter(group_name = group_name).order_by('-group_task_series')
        if tasks:
            task = tasks.first()
            group_series = task.group_series
            group_task_series = task.group_task_series + 1
            data.update({'group_series':group_series})
            data.update({'group_task_series':group_task_series})
        return data

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.format_put_request(request)
        serializer = self.get_serializer(instance, data=data, partial=True)
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
        scripts = self.request.query_params.get('scripts',None)
        if name:
            queryset = queryset.filter(name__iexact=name)
        if scripts:
            queryset = queryset.all()
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

class PowerStateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PowerState.objects.all()
    serializer_class = PowerStateSerializer
    permission_class = [permissions.IsAuthenticated,permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class GeneralQueryStringViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GeneralQueryString.objects.all()
    serializer_class =GeneralQueryStringSerializer
    permission_class = [permissions.IsAuthenticated,permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class TaskIssueViewSet(viewsets.ModelViewSet):
    queryset = TaskIssue.objects.all()
    serializer_class = TaskIssueSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.AllowAny]

    def perform_create(self, serializer):
        return super().perform_create(serializer)

    def format_post_request(self,request:Request):
        data={}
        title = request.data.get('title',None)
        level = request.data.get('level',None)
        task = request.data.get('task',None)
        power_state = request.data.get('power_state',None)
        device_driver = request.data.get('device_driver',None)
        function = request.data.get('function',None)
        description = request.data.get('description',None)
        if power_state:
            power_state = PowerState.objects.get(name__iexact=power_state).id
        data.update(
            {
                'title':title,
                'level':level,
                'task':task,
                'power_state':power_state,
                'device_driver':device_driver,
                'function':function,
                'description':description,
            }
        )
        return data

    def get_queryset(self):
        queryset = super().get_queryset()
        sn = self.request.query_params.get('sn',None)
        if sn:
            queryset = queryset.filter(task__uut__sn=sn)
        return queryset

    def create(self, request, *args, **kwargs):
        data = self.format_post_request(request)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def format_put_request(self,request:Request):
        data = request.data.copy()
        power_state = data.get('power_state',None)
        if power_state:
            power_state = PowerState.objects.get(name__iexact=power_state).id
            data.update({'power_state':power_state})
        return data

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.format_put_request(request)
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)





