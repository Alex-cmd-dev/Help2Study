from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Topic, Flashcard

"""
converts it from python to json
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class FlashcardSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ["id", "topic", "question", "answer", "created_at", "user"]
        extra_kwargs = {"user": {"read_only": True}}


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name", "created_at" , "user"]
        extra_kwargs = {"user": {"read_only": True} }
