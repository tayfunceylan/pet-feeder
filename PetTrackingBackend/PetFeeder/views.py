from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from rest_framework import generics
# Create your views here.


#   TODO: Adding Meal Rest API Endpoints
#   TODO: on Post-Request: associate it with a cat and a Food
#   TODO: on Get-Request: respond with all Meals.


class FoodList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class PetList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Pet.objects.all()
    serializer_class = PetSerializer


# ===================================================================================================
# ===========================[ Get, Update or Destroy a Detail Model ] ==============================
class PetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer


class FoodDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

