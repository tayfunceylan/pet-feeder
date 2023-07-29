from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from rest_framework import generics
# Create your views here.


class MealList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer


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


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer


class FoodDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

