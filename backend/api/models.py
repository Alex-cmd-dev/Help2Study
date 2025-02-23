from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_topics"
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="flashcards"
    )
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_flashcards"
    )  # deletes all the summaries the user has

    def __str__(self):
        return self.question
