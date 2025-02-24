from django.urls import path
from . import views


urlpatterns = [
    path('topics/', views.TopicListCreate.as_view(),name="topic-list"),
    path('topic/delete/<int:pk>', views.TopicDelete.as_view(),name="delete-topic"),
    path('flashcards/', views.FileUpload.as_view(),name="upload-file")
]