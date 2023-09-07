from rest_framework import serializers
from .models import Pet, Food, Meal
from rest_framework.serializers import ModelSerializer


class PetSerializer(ModelSerializer):
    # The name can only occur once and is handled in the views.py
    class Meta:
        model = Pet
        exclude = ["created_at"]

class FoodSerializer(ModelSerializer):
    left = serializers.IntegerField(read_only=True)
    class Meta:
        model = Food
        exclude = ["created_at"]

    @staticmethod
    def validate_name(value):
        if Food.objects.filter(name=value).exists():
            raise serializers.ValidationError("A Pet with this name already exists.")
        return value

class MealSerializer(ModelSerializer):
    class Meta:
        model = Meal
        exclude = ["created_at"]

class DailyMealSerializer(serializers.Serializer):
    date = serializers.DateField()
    meals = MealSerializer(many=True)  # `Meal` instances for that day
