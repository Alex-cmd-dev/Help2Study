from django.db import models
from django.contrib.auth.models import User







class Flashcard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="flashcards"
    )  # deletes all the summaries the user has

    def __str__(self):
        return self.question

