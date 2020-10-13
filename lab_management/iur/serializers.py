from django.contrib.auth.models import User,Group
from rest_framework import serializers
from .models import Uut

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= User
        fields = ['url','username','email','groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url','name']

class UutSerializer(serializers.HyperlinkedModelSerializer):
    platform = serializers.PrimaryKeyRelatedField(read_only=True,allow_null=True)
    class Meta:
        model = Uut
        fields = '__all__'