import json

from django.forms.models import model_to_dict
from rest_framework import status
from .test_setup import BasicTestCase


class MealTestCase(BasicTestCase):
    """
        Define All base variables: Url and test meal dictionary
    """
    base_url = '/Meal'
    new_Meal = {
        'food': 1,
        'pet': 1,
        'quantity': 100,
    }

    def test_Meal_get_list(self):
        """
            Test if the API can Get a Meal and check if the name, age and race is matching
        """
        response = self.client.get(f'{self.base_url}/')
        # validate response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.number_of_meals)
        self.check_equality(response.data['results'][0],
                            model_to_dict(self.test_meal),
                            ['quantity', 'food', 'pet'])
        # TODO: get the datetime
        print(f'test_Meal_get_list: OK')

    def test_create_new_Meal(self):
        """
            Test if we can create a new Meal and check if it's name, age and race are matching
        """
        response = self.client.post(f'{self.base_url}/', data=self.new_Meal)

        # validate initial response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.check_equality(response.data, self.new_Meal)
        self.assertEqual(response.data['id'], self.number_of_meals + 1)
        print('test_create_new_Meal: OK')

    def test_delete_Meal(self):
        """
            Test if we can delete a Meal and the counter is 0
        """
        fid = 1
        response = self.client.delete(f'{self.base_url}/{fid}/')
        # validate delete
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # validate if Meal has been successfully deleted
        response = self.client.get(f'{self.base_url}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.number_of_meals - 1)
        print("test_delete_Meal: OK")

    def test_update_pet_parameter(self):
        """
            Test if we can update the meal parameters accordingly
            We use the class defined meal, since we already have meal in the database
        """
        pid = self.number_of_meals
        response = self.client.put(f'{self.base_url}/{pid}/', data=self.new_Meal)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_equality(response.data, self.new_Meal)     # check if the new_pet data is the same as response.data
        self.assertEqual(response.data['id'], pid)      # also check if the ID is the same
        print('test_update_Meal_parameter: OK')