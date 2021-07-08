from django.contrib.auth.models import User,Group
from rest_framework import serializers
from .models import Uut,UutStatus,PlatformPhase,PlatformConfig,UutPhase,Platform,Member

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['url','username','email','groups']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url','name']

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model=Member
        fields='__all__'

class PlatformConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformConfig
        fields='__all__'

class UutPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UutPhase
        fields='__all__'
        
class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields='__all__'

class UutStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UutStatus
        fields='__all__'

class PlatformPhaseSerializer(serializers.ModelSerializer):
    phase = UutPhaseSerializer()
    platform = PlatformSerializer()
    config = PlatformConfigSerializer(required=False)
    class Meta:
        model = PlatformPhase
        fields='__all__'

class UutSerializer(serializers.ModelSerializer):
    status = UutStatusSerializer(required=False)
    platform_phase = PlatformPhaseSerializer(required=False)
    class Meta:
        model = Uut
        fields='__all__'

    def create(self, validated_data):
        
        return super().create(validated_data)



