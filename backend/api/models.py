from django.db import models
from django.contrib.auth.models import User


class Summary(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="summaries"
    )  # deletes all the summaries the user has

    def __str__(self):
        return self.title
