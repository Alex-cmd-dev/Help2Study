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

import logging
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from .serializers import UserSerializer, TopicSerializer, FlashcardSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Topic, Flashcard
from .geminiapi import handle_flashcard_creation

# ============================================
# LOGGING SETUP FOR PRESENTATION & DEBUGGING
# ============================================
# Logger for tracking request journey through the system
#
# WHY LOGGING IS IMPORTANT:
# 1. DEBUGGING: Helps identify where errors occur in the request flow
# 2. MONITORING: Track system behavior in production
# 3. LEARNING: Visualize how data moves through the application
# 4. PERFORMANCE: Measure how long operations take
#
# HOW TO USE:
# - logger.info() for normal operations (what we use for presentations)
# - logger.warning() for concerning but non-critical issues
# - logger.error() for errors that need attention
# - logger.debug() for detailed debugging info
#
# WHERE TO VIEW: When you run `python manage.py runserver`,
# logs appear in the terminal with 🔵 markers for easy tracking
#
# FUTURE USE: In production, logs go to files or monitoring services
# like AWS CloudWatch, DataDog, or Sentry for real-time alerts
logger = logging.getLogger('api')


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
        logger.info(f"REQUEST JOURNEY - STEP 3: Fetching topics for user: {user.username}")
        queryset = Topic.objects.filter(user=user)
        logger.info(f"DATABASE: Found {queryset.count()} topics")
        return queryset

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

        LOGGING NOTE: Each logger.info() statement below tracks a different
        stage of the request. This is invaluable for:
        - Presentations: Show the complete data flow to an audience
        - Debugging: Quickly identify which step failed
        - Learning: Understand the order of operations
        - Performance: Add timestamps to measure bottlenecks
        """
        # Visual separator makes logs easier to read
        logger.info("=" * 60)
        logger.info("REQUEST JOURNEY - STEP 3: POST request arrived at TopicListCreate view")

        # Validate the data structure
        serializer.is_valid(raise_exception=True)
        logger.info("VALIDATION: Data structure validated successfully")

        user = self.request.user
        logger.info(f"AUTHENTICATION: User '{user.username}' authenticated via JWT")

        # Save topic to database first (CREATE operation)
        topic_name = serializer.validated_data.get('name')
        logger.info(f"DATABASE - STEP 4: Creating new topic '{topic_name}'")
        topic = serializer.save(user=user)
        logger.info(f"DATABASE: Topic created with ID={topic.id}")

        # Extract file from multipart form data
        uploaded_file = self.request.data.get("file")
        if not uploaded_file:
            logger.error("ERROR: No file uploaded in request")
            raise serializers.ValidationError({"error": "No file uploaded"})

        logger.info(f"FILE UPLOAD: Received file '{uploaded_file.name}' ({uploaded_file.content_type})")

        # 🔵 REQUEST JOURNEY - STEP 5: Send to AI for processing
        # This function extracts text and generates flashcards
        logger.info("AI PROCESSING - STEP 5: Sending file to Gemini AI...")
        handle_flashcard_creation(uploaded_file, topic, user)
        logger.info("AI PROCESSING: Flashcards generated successfully")
        logger.info("RESPONSE - STEP 6: Sending JSON response back to frontend")
        logger.info("=" * 60)


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
