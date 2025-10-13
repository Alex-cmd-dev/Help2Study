"""
API URL ROUTING - The "Order System" Menu in our Restaurant

This file maps URL patterns to view handlers.
When a request arrives, Django matches the URL and calls the appropriate view.

🔵 REQUEST JOURNEY - STEP 3: URLs route requests to views

CONCEPTS: Routing, URL patterns, Endpoints
RELATED: views.py (handlers), backend/urls.py (main router)

URL STRUCTURE: /api/ + these patterns
Example: POST /api/topics/ → calls TopicListCreate view
"""

from django.urls import path
from . import views

urlpatterns = [
    # GET /api/topics/ - List all topics
    # POST /api/topics/ - Create new topic + upload file
    path('topics/', views.TopicListCreate.as_view(), name="topic-list"),

    # DELETE /api/topic/delete/5 - Delete topic with id=5
    # <int:pk> captures the topic ID from the URL
    path('topic/delete/<int:pk>', views.TopicDelete.as_view(), name="delete-topic"),

    # GET /api/flashcards/5/ - Get all flashcards for topic id=5
    # <int:topic_id> captures and passes to the view
    path('flashcards/<int:topic_id>/', views.FlashcardListByTopic.as_view(), name="flashcards-by-topic"),
]