import json

from django.forms.models import model_to_dict
from rest_framework import status

from .test_setup import BasicTestCase


class FoodTestCase(BasicTestCase):
    """
    Define All base variables: Url and test food dictionary
    """

    base_url = "/api/food"
    new_Food = {
        "name": "Food2",
        "brand": "mellow",
        "price": 10,
        "category": "D",
        "unit": "g",
    }

    def test_Food_get_list(self):
        """
        Test if the API can Get a Food and check if the name, age and race is matching
        """
        response = self.client.get(f"{self.base_url}/")
        # validate response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), self.number_of_foods)
        self.check_equality(response.data["results"][0], model_to_dict(self.test_food))
        print(f"test_Food_get_list: OK")

    def test_create_new_Food(self):
        """
        Test if we can create a new Food and check if it's name, age and race are matching
        """
        response = self.client.post(f"{self.base_url}/", data=self.new_Food)

        # validate initial response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.check_equality(response.data, self.new_Food)
        self.assertEqual(response.data["id"], self.number_of_foods + 1)
        print("test_create_new_Food: OK")

    def test_delete_Food(self):
        """
        Test if we can delete a Food and the counter is 0
        """
        fid = 1
        response = self.client.delete(f"{self.base_url}/{fid}/")
        # validate delete
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # validate if Food has been successfully deleted
        response = self.client.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), self.number_of_foods - 1)
        print("test_delete_Food: OK")

    def test_update_pet_parameter(self):
        """
        Test if we can update the food parameters accordingly
        We use the class defined food, since we already have food in the database
        """
        pid = self.number_of_foods
        response = self.client.put(f"{self.base_url}/{pid}/", data=self.new_Food)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_equality(
            response.data, self.new_Food
        )  # check if the new_pet data is the same as response.data
        self.assertEqual(response.data["id"], pid)  # also check if the ID is the same
        print("test_update_Food_parameter: OK")
