from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from rest_framework import status
from api.models import Pet, Meal, Food


class BasicTestCase(APITestCase):
    def setUp(self) -> None:
        # Create User and Login
        self.password = "test"
        self.username = "test-user"
        self.test_user = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.client.login(username=self.username, password=self.password)
        # Create Pets, food and meals
        self.number_of_pets = 1
        self.number_of_foods = 1
        self.number_of_meals = 1
        self.test_pet = Pet.objects.create(name="Pet1", age=2, race="cat")
        self.test_food = Food.objects.create(
            name="test_food",
            brand="test_brand",
            category="Dry",
            price=10,
            unit="g",
        )
        self.test_meal = Meal(
            quantity=100,
            food_id=1,
        )

        # save data
        self.test_meal.save()
        self.test_food.save()
        self.test_pet.save()
        self.test_user.save()
        self.test_meal.pets.add(self.test_pet)

    def check_equality(self, response_data: dict, input_data: dict, keys=None):
        key_list = keys if type(keys) == list else input_data.keys()
        for key in key_list:
            self.assertEqual(response_data[key], input_data[key])

    def get_token(self):
        user = {
            "username": self.test_user.username,
            "password": self.password,
        }
        response = self.client.post(f"/api-token/", data=user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access"]
        self.header_token = {"Authorization": f"Bearer {self.token}"}
        return {"Authorization": f"Bearer {self.token}"}
