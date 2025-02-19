from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import UserSerializer, SummarySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Summary
from .filetotext import processfile


# creates new user
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class SummaryListCreate(generics.ListCreateAPIView):
    serializer_class = SummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user1 = self.request.user
        return Summary.objects.filter(user=user1)

    def perform_create(self, serializer):
        if serializer.isvalid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)


class SummaryDelete(generics.DestroyAPIView):
    serializer_class = SummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user1 = self.request.user
        return Summary.objects.filter(user=user1)


class FileUpload(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        uploaded_file = request.FILES.get("file")
        title = request.data.get("title")
        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=400)
        try:
            summary_text = processfile(uploaded_file)
            summary = Summary.objects.create(
                user=request.user, content=summary_text, title=title
            )
            serializer = SummarySerializer(summary)
            return Response(serializer.data, status=201)

        except Exception as e:
            return Response({"error": f"Processing failed: {str(e)}"}, status=500)
