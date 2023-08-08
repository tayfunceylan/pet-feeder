from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from .models import Pet, Food, Meal
from rest_framework.serializers import ModelSerializer


class PetSerializer(ModelSerializer):
    # The name can only occur once and is handled in the views.py
    class Meta:
        model = Pet
        fields = '__all__'


class FoodSerializer(ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

    @staticmethod
    def validate_name(value):
        if Food.objects.filter(name=value).exists():
            raise serializers.ValidationError("A Pet with this name already exists.")
        return value


class MealSerializer(ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'


class DailyMealSerializer(serializers.Serializer):
    date = serializers.DateField()
    meals = MealSerializer(many=True)  # `Meal` instances for that day

