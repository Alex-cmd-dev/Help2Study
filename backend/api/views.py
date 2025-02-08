from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer,SummarySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Summary


#creates new user
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

        
        
