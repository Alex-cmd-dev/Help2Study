"""
API VIEWS - The "Kitchen Staff" in our Restaurant

Views are request handlers - they receive HTTP requests, process them, and return responses.
This is where the business logic lives!

ROLE IN REQUEST CYCLE:
1. Request arrives → Django routing sends it here (via urls.py)
2. View authenticates user (checks JWT token)
3. View validates data (using serializers)
4. View interacts with database (via models/ORM)
5. View prepares response and sends back JSON

CONCEPTS: REST API, HTTP Methods, Class-Based Views, Authentication, CRUD
RELATED: urls.py (routes to these views), models.py (database), serializers.py (validation)
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from .serializers import UserSerializer, TopicSerializer, FlashcardSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Topic, Flashcard
from .geminiapi import handle_flashcard_creation


class CreateUserView(generics.CreateAPIView):
    """
    ENDPOINT: POST /api/user/register/
    PURPOSE: Create a new user account

    PERMISSION: AllowAny (anyone can register, no authentication needed)
    HTTP METHOD: POST only

    REQUEST BODY: { "username": "...", "password": "...", "email": "..." }
    RESPONSE: 201 Created with user data
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Public endpoint


class TopicListCreate(generics.ListCreateAPIView):
    """
    ENDPOINT: GET /api/topics/ or POST /api/topics/
    PURPOSE: List all user's topics OR create new topic with flashcards

    PERMISSION: IsAuthenticated (must have valid JWT token)
    HTTP METHODS:
    - GET: Returns list of user's topics
    - POST: Creates topic + generates flashcards from uploaded file

    🔵 REQUEST JOURNEY - STEP 3: This is where file uploads arrive!
    """
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]  # Must be logged in

    def get_queryset(self):
        """
        GET request handler - returns only THIS user's topics

        CONCEPT: Query filtering with ORM
        SQL equivalent: SELECT * FROM topics WHERE user_id = ?

        This ensures users can only see their own topics (security!)
        """
        user = self.request.user
        return Topic.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        POST request handler - creates topic and flashcards

        🔵 REQUEST JOURNEY - STEP 4: Processing the upload
        Flow:
        1. Validate incoming data
        2. Save topic to database
        3. Extract uploaded file
        4. Send file to Gemini AI for processing
        5. AI creates flashcards (happens in geminiapi.py)

        CONCEPTS: File handling, Data validation, External API integration
        """
        # Validate the data structure
        serializer.is_valid(raise_exception=True)

        user = self.request.user

        # Save topic to database first (CREATE operation)
        topic = serializer.save(user=user)

        # Extract file from multipart form data
        uploaded_file = self.request.data.get("file")
        if not uploaded_file:
            raise serializers.ValidationError({"error": "No file uploaded"})

        # 🔵 REQUEST JOURNEY - STEP 5: Send to AI for processing
        # This function extracts text and generates flashcards
        handle_flashcard_creation(uploaded_file, topic, user)


class TopicDelete(generics.DestroyAPIView):
    """
    ENDPOINT: DELETE /api/topics/<id>/delete/
    PURPOSE: Delete a topic and all its flashcards

    PERMISSION: IsAuthenticated
    HTTP METHOD: DELETE only

    CONCEPT: CASCADE deletion - deleting a topic automatically
    deletes all related flashcards (defined in models.py)
    """
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Security: users can only delete their own topics
        user = self.request.user
        return Topic.objects.filter(user=user)


class FlashcardListCreate(generics.ListCreateAPIView):
    """
    ENDPOINT: GET or POST /api/flashcards/
    PURPOSE: List flashcards for a topic OR create new flashcard

    PERMISSION: IsAuthenticated
    HTTP METHODS: GET (with ?topic=name query param), POST
    """
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        """
        Filter flashcards by topic name from query parameters
        Example: /api/flashcards/?topic=Math
        """
        user = self.request.user
        topic_name = self.request.query_params.get("topic")
        return Flashcard.objects.filter(user=user, topic__name=topic_name)

    def perform_create(self, serializer):
        """Manually create a single flashcard (used rarely)"""
        topic_id = self.request.data.get("id")
        user = self.request.user
        topic = Topic.objects.get(user=user, id=topic_id)
        if serializer.is_valid():
            serializer.save(user=user, topic=topic)
        else:
            print(serializer.errors)


class FlashcardDelete(generics.DestroyAPIView):
    """
    ENDPOINT: DELETE /api/flashcards/<id>/
    PURPOSE: Delete a single flashcard

    PERMISSION: IsAuthenticated
    HTTP METHOD: DELETE only
    """
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(user=user)


class FlashcardListByTopic(APIView):
    """
    ENDPOINT: GET /api/flashcards/<topic_id>/
    PURPOSE: Get all flashcards for a specific topic

    PERMISSION: IsAuthenticated (checked automatically)
    HTTP METHOD: GET only

    🔵 REQUEST JOURNEY - STEP 6: This returns data to the frontend
    """
    def get(self, request, topic_id):
        """
        Fetch flashcards and return as JSON

        CONCEPTS: ORM query, Serialization, HTTP Response
        """
        # Get topic (or 404 if not found/not owned by user)
        topic = get_object_or_404(Topic, id=topic_id, user=self.request.user)

        # Query all flashcards for this topic (READ operation)
        flashcards = Flashcard.objects.filter(topic=topic)

        # Convert Python objects → JSON
        serializer = FlashcardSerializer(flashcards, many=True)

        # Return HTTP response with JSON data
        return Response(serializer.data)
