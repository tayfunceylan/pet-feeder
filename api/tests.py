from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from rest_framework import status
from .models import Pet, Meal, Food

class PetTestCase(APITestCase):
    """

    """
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username="test-user", password="test")
        self.client.login(username="test-user", password="test")
        self.test_pet = Pet.objects.create(name="Pet1", age=2, race="cat")
        self.number_of_pets = 1
        self.base_url = '/Pet/'

    def test_pet_get_list(self):
        """
            Test if the API can Get a Pet and check if the name, age and race is matching
        """
        response = self.client.get(self.base_url)
        # validate response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(json.dumps(response.data))      # view response as JSON format
        # Validate response data
        self.assertEqual(response.data['count'], self.number_of_pets)
        self.assertEqual(response.data['results'][0]['name'], self.test_pet.name)
        self.assertEqual(response.data['results'][0]['age'], self.test_pet.age)
        self.assertEqual(response.data['results'][0]['race'], self.test_pet.race)
        print(f'get_pet_list: ok')

    def test_create_new_pet(self):
        """
            Test if we can create a new pet and check if it's name, age and race are matching
        """
        new_pet = {'name': 'Pet2', 'age': 3, 'race': 'dog'}
        response = self.client.post(self.base_url, data=new_pet)

        # validate initial response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_pet['name'])
        self.assertEqual(response.data['age'], new_pet['age'])
        self.assertEqual(response.data['race'], new_pet['race'])
        self.assertEqual(response.data['id'], self.number_of_pets + 1)
        print('create_new_pet: ok')

    def test_delete_pet(self):
        """
            Test if we can delete a pet and the counter is 0
        """
        pk = 1
        response = self.client.delete(f'{self.base_url}{pk}/')
        # validate delete
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # validate if a pet has been successfully deleted
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.number_of_pets - 1)
        print("delete_pet_with_id: ok")

    def test_get_meal_from_pet(self):
        """
            Test if you can search the meal through the Pet id
        """
        new_food, new_meal = self.create_food_meal()
        response = self.client.get(f'{self.base_url}get_meals/?PID=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # validate if the request is correct
        self.assertEqual(response.data['pet'], model_to_dict(self.test_pet))
        self.assertEqual(response.data['meals'][0]['quantity'], model_to_dict(new_meal)['quantity'])
        self.assertEqual(response.data['meals'][0]['pet'], model_to_dict(new_meal)['pet'])
        self.assertEqual(response.data['meals'][0]['food'], model_to_dict(new_meal)['food'])
        print(f'get_meals_through_pet_id (PID)')

    @staticmethod
    def create_food_meal():
        new_food = Food.objects.create(
            name='test_food',
            brand='test_brand',
            category='Dry',
            price=10,
            unit='g',
        )
        new_meal = Meal.objects.create(
            food_id=1,
            pet_id=1,
            quantity=100,
        )
        return new_food, new_meal


