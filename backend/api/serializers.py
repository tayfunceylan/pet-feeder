from rest_framework import serializers
from .models import Pet, Food, Meal, Schedule
from rest_framework.serializers import ModelSerializer


class PetSerializer(ModelSerializer):
    picture = serializers.ImageField(max_length=None, use_url=False, required=False)
    class Meta:
        model = Pet
        exclude = ["created_at"]

class FoodSerializer(ModelSerializer):
    left = serializers.IntegerField(read_only=True)
    top_quantities = serializers.ListField(read_only=True)
    class Meta:
        model = Food
        exclude = ["created_at"]

class MealSerializer(ModelSerializer):
    class Meta:
        model = Meal
        exclude = ["created_at"]

class ScheduleSerializer(ModelSerializer):
    # 0b11111 00001010 00000000 00000010 00000001
    export_schedule = serializers.CharField(read_only=True)
    class Meta:
        model = Schedule
        exclude = ["created_at"]