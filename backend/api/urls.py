from django.urls import path
from . import views


urlpatterns = [
    path('summaries/', views.SummaryListCreate.as_view(),name="summary-list"),
    path('summaries/delete/<int:pk>', views.SummaryDelete.as_view(),name="delete-summary"),
    path('summarize/', views.FileUpload.as_view(),name="process-file")
]