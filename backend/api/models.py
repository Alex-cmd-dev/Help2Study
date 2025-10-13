"""
DATABASE MODELS - The "Pantry Organization" in our Restaurant

This file defines the structure of our database using Django's ORM (Object-Relational Mapper).
Each class represents a table, and each attribute represents a column.

ROLE IN THE SYSTEM:
- Defines what data we store (users, topics, flashcards)
- Establishes relationships between data (e.g., a topic belongs to a user)
- Provides a Python interface to the database (no SQL needed!)

CONCEPTS: Models, ORM, Foreign Keys, Database Relationships, CRUD
RELATED: views.py (uses these models), serializers.py (converts to JSON)
"""

from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """
    Represents a collection of flashcards organized by subject.

    RELATIONSHIP: One user can have many topics (One-to-Many)
    DATABASE TABLE: api_topic
    """
    # Foreign Key = "This topic belongs to one user"
    # on_delete=CASCADE = "If user is deleted, delete their topics too"
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_topics"
    )

    # CharField = text with max length
    name = models.CharField(max_length=255)

    # auto_now_add = automatically set when created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # How this object appears in Django admin and logs
        return self.name


class Flashcard(models.Model):
    """
    Represents a single question-answer pair.

    RELATIONSHIPS:
    - Belongs to one Topic (Many-to-One)
    - Belongs to one User (Many-to-One)

    DATABASE TABLE: api_flashcard
    """
    # This flashcard belongs to a topic
    # If topic is deleted, delete all its flashcards
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="flashcards"
    )

    # TextField = unlimited text length
    question = models.TextField()
    answer = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    # Also track which user created it
    # If user is deleted, delete all their flashcards
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_flashcards"
    )

    def __str__(self):
        return self.question
