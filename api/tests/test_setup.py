from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from rest_framework import status
from api.models import Pet, Meal, Food


class BasicTestCase(APITestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username="test-user", password="test")
        self.client.login(username="test-user", password="test")
        self.number_of_pets = 1
        self.number_of_foods = 1
        self.number_of_meals = 1
        self.test_pet = Pet.objects.create(
            name="Pet1",
            age=2,
            race="cat"
        )
        self.test_food = Food.objects.create(
            name='test_food',
            brand='test_brand',
            category='Dry',
            price=10,
            unit='g',
        )
        self.test_meal = Meal.objects.create(
            food_id=1,
            pet_id=1,
            quantity=100,
        )

    def check_equality(self, response_data: dict, input_data: dict, keys=None):
        key_list = keys if type(keys) == list else input_data.keys()
        for key in key_list:
            self.assertEqual(response_data[key], input_data[key])
