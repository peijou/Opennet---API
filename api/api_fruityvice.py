import requests
from requests import Response


class Fruityvice:
    """
    Get Fruityvice api
    """
    def __init__(self):
        self.url = "https://www.fruityvice.com/"
        self.search = "api/fruit/"
        self.headers = {}
        self.payload = {}

    def get_fruit_all(self) -> Response:
        """
        Get all fruit data from api

        :return: api response
        """
        url = f"{self.url}{self.search}all"
        response = requests.get(url, headers=self.headers, data=self.payload)
        return response

    def search_fruit_by_name(self, name: str) -> Response:
        """
        Search fruit data by name

        :param name: string, for example, "Persimmon"
        :return: api response
        """
        url = f"{self.url}{self.search}{name}"
        response = requests.get(url, headers=self.headers, data=self.payload)
        return response

    def search_nutrition_criteria(self, nutrition: str, min_: float = 0, max_: float = 1000) -> Response:
        """
        Search a specific nutrition's value which between min and max

        :param nutrition: string, for example, "carbohydrates", "protein", "fat"
        :param min_: float, default is 0
        :param max_: float, default is 1000
        :return: api response
        """
        url = f"{self.url}{self.search}{nutrition}?min={min_}&max={max_}"
        print(url)
        response = requests.get(url, headers=self.headers, data=self.payload)
        return response

