"""
SERIALIZERS - The "Translators" in our Restaurant

Serializers convert data between formats:
- Python objects → JSON (for API responses)
- JSON → Python objects (for incoming requests)

They also validate incoming data before it reaches the database.

ROLE IN REQUEST CYCLE:
- REQUEST: JSON → Serializer validates → Python object → Saved to DB
- RESPONSE: DB query → Python object → Serializer → JSON

CONCEPTS: Serialization, Data Validation, JSON conversion
RELATED: views.py (uses serializers), models.py (source of data)
"""

import logging
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Topic, Flashcard

# ============================================
# LOGGING FOR DATA TRANSFORMATION TRACKING
# ============================================
# Logger for tracking how data changes format as it moves through the system
#
# WHY LOG IN SERIALIZERS:
# Serializers are the "translators" that convert data between formats.
# Logging here helps you see:
# - What the Python object looks like before conversion
# - What the JSON looks like after conversion
# - Any data transformations or calculations that happen
#
# REAL-WORLD EXAMPLE:
# When you call an API endpoint, you want to verify the exact JSON
# being sent to the frontend. Logging in serializers shows you this!
#
# FUTURE USE: In production, you might log to track:
# - What data users are accessing
# - How often certain fields are null
# - Performance issues with large datasets
logger = logging.getLogger('api')


class UserSerializer(serializers.ModelSerializer):
    """
    Converts User model ↔ JSON for registration/login

    SECURITY: Password is write_only (never sent in responses)
    """
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}  # Don't return password!

    def create(self, validated_data):
        """
        Create user with hashed password
        create_user() automatically hashes the password for security
        """
        user = User.objects.create_user(**validated_data)
        return user


class FlashcardSerializer(serializers.ModelSerializer):
    """
    Converts Flashcard model ↔ JSON

    USAGE:
    - GET responses: Python Flashcard object → JSON
    - POST requests: JSON → validate → Python object
    """
    class Meta:
        model = Flashcard
        fields = ["id", "topic", "question", "answer", "created_at", "user"]
        extra_kwargs = {"user": {"read_only": True}}  # User set from JWT token


class TopicSerializer(serializers.ModelSerializer):
    """
    Converts Topic model ↔ JSON

    🔵 REQUEST JOURNEY - STEP 5: This converts the response to JSON
    """
    class Meta:
        model = Topic
        fields = ["id", "name", "created_at", "user"]
        extra_kwargs = {"user": {"read_only": True}}  # User set from JWT token

    def to_representation(self, instance):
        """
        Convert Python object → JSON for response
        Called when sending data back to frontend

        LOGGING NOTE: This method is automatically called by Django REST Framework
        whenever a Topic needs to be converted to JSON for an API response.
        By logging here, you can see:
        - The exact JSON structure being sent to the frontend
        - The ID of the object being converted
        - Any custom transformations you might add in the future

        FUTURE USE: You might extend this method to:
        - Add computed fields (e.g., flashcard count)
        - Format dates differently
        - Hide sensitive information
        """
        data = super().to_representation(instance)
        logger.info(f"SERIALIZATION: Converting Topic(id={instance.id}) → JSON")
        logger.info(f"JSON OUTPUT: {data}")
        return data
