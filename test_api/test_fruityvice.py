import pytest
from pytest_assume.plugin import assume

from api.api_fruityvice import Fruityvice


class TestFruityviceApi:
    """
    API Document: https://www.fruityvice.com/doc/index.html#api-GET-GET
    """

    def test_get_all_fruit(self):
        """
        Verify the api can get all fruit data
        """
        fruityvice = Fruityvice()
        fv_all_api = fruityvice.get_fruit_all()

        assert (
            fv_all_api.status_code == 200
        ), f"{fv_all_api.status_code=}, {fv_all_api.text=}"

    @pytest.mark.parametrize(
        "name, exp_status_code",
        [
            ("Persimmon", 200),
            ("123", 404),
            (" ", 404),
            ("  banana", 404),
            ("Select *", 404),
        ],
    )
    def test_fruit_search_result(self, name: str, exp_status_code: int):
        """
        Varify the status code is the same as their document
        """
        fruityvice = Fruityvice()
        fv_search_api = fruityvice.search_fruit_by_name(name)

        # Verify status code
        with assume:
            assert (
                fv_search_api.status_code == exp_status_code
            ), f"{fv_search_api.status_code=}, {fv_search_api.text=}"

        # Verify 404 error msg & fruit data correctness
        if fv_search_api.status_code == 404:
            with assume:
                assert fv_search_api.text == '{"error":"Not found"}'
        elif fv_search_api.status_code == 200:
            with assume:
                assert fv_search_api.json()["name"] == name, f"{fv_search_api.text=}"

    @pytest.mark.parametrize(
        "nutrition, min_, max_, exp_status_code",
        [("protein", 1, 1, 200), ("fat", 0, 0.5, 200), ("fat", 5, 0, 404)],
    )
    def test_nutrition_criteria(self, nutrition, min_, max_, exp_status_code):
        """
        Verify the status code and the correctness of nutrition criteria
        """
        fruityvice = Fruityvice()
        fv_nutrition_api = fruityvice.search_nutrition_criteria(
            nutrition=nutrition, min_=min_, max_=max_
        )

        # Verify status code
        with assume:
            assert (
                fv_nutrition_api.status_code == exp_status_code
            ), f"{fv_nutrition_api.status_code=}, {fv_nutrition_api.text=}"

        # Verify the nutrition value is between min and max & 404 error msg
        if fv_nutrition_api.status_code == 200:
            nutrition_lst = fv_nutrition_api.json()
            for i in range(len(nutrition_lst)):
                with assume:
                    assert (
                        nutrition_lst[i]["nutritions"][nutrition] >= min_
                    ), f"{nutrition_lst[i][nutrition]=} !>= {min_}"
                with assume:
                    assert (
                        nutrition_lst[i]["nutritions"][nutrition] <= max_
                    ), f"{nutrition_lst[i][nutrition]=} !<= {max_}"
        elif fv_nutrition_api.status_code == 404:
            with assume:
                assert (
                    fv_nutrition_api.text
                    == '{"error":"No fruits with given nutritional parameter found"}'
                ), f"{fv_nutrition_api.text=}"
