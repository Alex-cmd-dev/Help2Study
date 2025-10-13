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

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Topic, Flashcard


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
