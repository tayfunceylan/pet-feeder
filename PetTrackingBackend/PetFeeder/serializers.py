from rest_framework import serializers

from .models import Pet, Food, Meal
from rest_framework.serializers import ModelSerializer


class PetSerializer(ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

    @staticmethod
    def validate_name(value):
        if Pet.objects.filter(name=value).exists():
            raise serializers.ValidationError("A Pet with this name already exists.")
        return value


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

