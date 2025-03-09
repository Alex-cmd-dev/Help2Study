from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import UserSerializer, TopicSerializer, FlashcardSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Topic, Flashcard
from .geminiapi import handle_flashcard_creation


# creates new user
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class TopicListCreate(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(user=user)

    def perform_create(self, serializer):
            serializer.is_valid(raise_exception=True)
            user = self.request.user
            topic = serializer.save(user=user)
            uploaded_file = self.request.data.get("file")
            if not uploaded_file:
                raise serializers.ValidationError({"error": "No file uploaded"})
            handle_flashcard_creation(uploaded_file, topic, user)


class TopicDelete(generics.DestroyAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(user=user)


class FlashcardListCreate(generics.ListCreateAPIView):
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        user = self.request.user
        topic_name = self.request.query_params.get("topic")  # get requests
        return Flashcard.objects.filter(user=user, topic__name=topic_name)

    def perform_create(self, serializer):
        topic_id = self.request.data.get("id")
        user = self.request.user
        topic = Topic.objects.get(user=user, id=topic_id)
        if serializer.is_valid():
            serializer.save(user=user, topic=topic)
        else:
            print(serializer.errors)


class FlashcardDelete(generics.DestroyAPIView):
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(user=user)


class FlashcardListByTopic(APIView):
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, id=topic_id, user=self.request.user)
        flashcards = Flashcard.objects.filter(topic=topic)
        serializer = FlashcardSerializer(flashcards, many=True)
        return Response(serializer.data)
