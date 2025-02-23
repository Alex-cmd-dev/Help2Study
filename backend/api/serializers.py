from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Summary

'''
converts it from python to json
'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","password"]
        extra_kwargs = {"password" : {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ["id","title","content","created_at","user"]
        extra_kwargs = {"user":{"read_only":True}}

class Flash