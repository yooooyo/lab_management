from rest_framework import serializers
from .models import DriverCategory, Task,Script,TaskStatus,Ap,Tool,Module,PowerState,TaskFunction,TaskIssue,Driver,DriverCategory
from iur.serializers import MemberSerializer, UutSerializer


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields='__all__'

class ApSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ap
        fields='__all__'
class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields='__all__'

class ScriptSerializer(serializers.ModelSerializer):
    tool = ToolSerializer()
    class Meta:
        model = Script
        fields='__all__'

class ModuleSerializer(serializers.ModelSerializer):
    owner = MemberSerializer(many=True)
    class Meta:
        model = Module
        fields='__all__'

class DriverCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverCategory
        fields='__all__'

class DriverSerializer(serializers.ModelSerializer):
    owner = MemberSerializer()
    class Meta:
        model = Driver
        fields='__all__'

class PowerStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerState
        fields='__all__'

class TaskFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFunction
        fields='__all__'

class TaskIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskIssue
        fields='__all__'

class TaskSerializer(serializers.ModelSerializer):
    # uut = UutSerializer()
    # script = ScriptSerializer()
    # status = TaskStatusSerializer()
    # ap = ApSerializer()
    # assigner = MemberSerializer()
    # script = serializers.PrimaryKeyRelatedField(queryset=Script.objects.all(),required=False)
    # status = serializers.PrimaryKeyRelatedField(queryset=TaskStatus.objects.all(),required=False)
    class Meta:
        model = Task
        fields='__all__'
    
    def create(self, validated_data):
        
        return Task.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.uut = validated_data.get('uut',instance.uut)
        instance.uut_uuid = validated_data.get('uut_uuid',instance.uut_uuid)
        instance.script = validated_data.get('script',instance.script)
        instance.status = validated_data.get('status',instance.status)
        instance.ap = validated_data.get('ap',instance.ap)
        instance.assigner = validated_data.get('assigner',instance.assigner)
        instance.task_group = validated_data.get('task_group',instance.task_group)
        instance.group_series = validated_data.get('group_series',instance.group_series)
        instance.uut_info = validated_data.get('uut_info',instance.uut_info)
        instance.power_cycle_info = validated_data.get('power_cycle_info',instance.power_cycle_info)
        instance.start_time = validated_data.get('start_time',instance.start_time)
        instance.finish_time = validated_data.get('finish_time',instance.finish_time)
        instance.log = validated_data.get('log',instance.log)
        instance.save()
        return instance


