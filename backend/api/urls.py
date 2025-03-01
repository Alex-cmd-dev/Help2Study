from django.urls import path
from . import views


urlpatterns = [
    path('topics/', views.TopicListCreate.as_view(),name="topic-list"),
    path('topic/delete/<int:pk>', views.TopicDelete.as_view(),name="delete-topic"),
    path('createflashcards/<int:topic_id>/', views.CreateFlashcards.as_view(),name="create-flashcards"),
    path('flashcards/<int:topic_id>/', views.FlashcardListByTopic.as_view(), name="flashcards-by-topic"),
]