from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import UserSerializer, TopicSerializer, FlashcardSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Topic, Flashcard
from geminiapi import create_flashcards, processfile
import os


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


class CreateFlashcards(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, topic_id):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response(
                {"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST
            )
        mime_type = uploaded_file.content_type
        file_path = None

        try:
            topic = Topic.objects.get(id=topic_id)
            file_path = processfile(uploaded_file)
            flashcards = create_flashcards(file_path, mime_type)

            created_flashcards = []
            for flashcard in flashcards:
                fcard = Flashcard.objects.create(
                    user=request.user,
                    topic=topic,
                    question=flashcard["question"],
                    answer=flashcard["answer"],
                )
                created_flashcards.append(fcard)

            # Clean up the temporary file
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

            # Use proper serializer with many=True for multiple objects
            serializer = FlashcardSerializer(created_flashcards, many=True)

            return Response(
                {
                    "success": f"Created {len(created_flashcards)} flashcards",
                    "flashcards": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Topic.DoesNotExist:
            return Response(
                {"error": f"Topic with id {topic_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            # Clean up the temporary file in case of errors
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                return Response(
                    {"error": f"Processing failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


class FlashcardListByTopic(APIView):
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, id=topic_id)
        flashcards = Flashcard.objects.filter(topic=topic)
        serializer = FlashcardSerializer(flashcards, many=True)
        return Response(serializer.data)
