import json

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from rest_framework import status
from api.models import Pet, Meal, Food
from .test_setup import BasicTestCase


class PetTestCase(BasicTestCase):
    """

    """
    base_url = '/Pet'

    def test_pet_get_list(self):
        """
            Test if the API can Get a Pet and check if the name, age and race is matching
        """
        response = self.client.get(f'{self.base_url}/')
        # validate response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.number_of_pets)
        self.check_equality(response.data['results'][0], model_to_dict(self.test_pet))
        print(f'test_pet_get_list: OK')

    def test_create_new_pet(self):
        """
            Test if we can create a new pet and check if it's name, age and race are matching
        """
        new_pet = {'name': 'Pet2', 'age': 3, 'race': 'dog'}
        response = self.client.post(f'{self.base_url}/', data=new_pet)

        # validate initial response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.check_equality(response.data, new_pet)
        self.assertEqual(response.data['id'], self.number_of_pets + 1)
        print('test_create_new_pet: OK')

    def test_delete_pet(self):
        """
            Test if we can delete a pet and the counter is 0
        """
        pk = 1
        response = self.client.delete(f'{self.base_url}/{pk}/')
        # validate delete
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # validate if a pet has been successfully deleted
        response = self.client.get(f'{self.base_url}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.number_of_pets - 1)
        print("test_delete_pet: OK")

    def test_cannot_post_two_pets_with_same_name(self):
        new_pet = {'name': 'double_pet',
                   'age': 5,
                   'race': 'cat'}
        response = self.client.post(f'{self.base_url}/', data=new_pet)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create the second pet with the same name. this should not be possible!!
        second_response = self.client.post(f'{self.base_url}/', data=new_pet)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        print("test_cannot_post_two_pets_with_same_name: OK")

    def test_update_pet_parameter(self):
        new_pet = {'name': 'new_name',
                   'age': 0,
                   'race': 'new_race'}
        pid = self.number_of_pets
        response = self.client.put(f'{self.base_url}/{pid}/', data=new_pet)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_equality(response.data, new_pet)     # check if the new_pet data is the same as response.data
        self.assertEqual(response.data['id'], pid)      # also check if the ID is the same
        print('test_update_pet_parameter: OK')

    def test_get_meal_from_pet(self):
        """
            Test if you can search the meal through the Pet id
        """
        new_food, new_meal = self.test_food, self.test_meal
        response = self.client.get(f'{self.base_url}/get_meals/?PID=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # validate if the request is correct
        self.assertEqual(response.data['pet'], model_to_dict(self.test_pet))
        self.check_equality(response.data['meals'][0], model_to_dict(new_meal), ['quantity', 'pet', 'food'])
        print(f'test_get_meal_from_pet (PID): OK')

    # noinspection DuplicatedCode
    def test_cannot_get_meal_from_not_existing_pet(self):
        response = self.client.get(f'{self.base_url}/get_meals/?PID=999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print(f'test_cannot_get_meal_from_not_existing_pet (PID): OK')







