from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import UserSerializer, TopicSerializer, FlashcardSerialzer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Topic, Flashcard
from geminiapi import processfile


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
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)


class TopicDelete(generics.DestroyAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(user=user)


class FlashcardListCreate(generics.ListCreateAPIView):
    serializer_class = FlashcardSerialzer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        topic_name = self.request.query_params.get("topic") #get requests
        return Flashcard.objects.filter(user=user,topic__name=topic_name)
    
    def perform_create(self, serializer):
        topic_id = self.request.data.get("id")
        user = self.request.user
        topic = Topic.objects.get(user=user, id=topic_id)
        if serializer.is_valid():
            serializer.save(user=user,topic = topic)
        else:
            print(serializer.errors)

class FlashcardDelete(generics.DestroyAPIView):
    serializer_class = FlashcardSerialzer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(user=user)


class CreateFlashcards(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        uploaded_file = request.FILES.get("file")
        title = request.data.get("topic")
        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=400)
        try:
            summary_text = processfile(uploaded_file)
            summary = Summary.objects.create(
                user=request.user, content=summary_text, title=title
            )
            serializer = SummarySerializer(summary)
            return Response(serializer.data, status=201)

        except Exception as e:
            return Response({"error": f"Processing failed: {str(e)}"}, status=500)
