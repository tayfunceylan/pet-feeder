from .models import Pet, Food, Meal
from rest_framework.serializers import ModelSerializer


class PetSerializer(ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'


class FoodSerializer(ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class MealSerializer(ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

