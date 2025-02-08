from django.urls import path
from . import views
from backend.api.summary import processfile


urlpatterns = [
    path('summaries/', views.SummaryListCreate.as_view(),name="note-list"),
    path('summaries/delete/<int:pk>', views.SummaryDelete.as_view(),name="delete-summary"),
    path('summarize', processfile,name="process-file")
]