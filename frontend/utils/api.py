import requests

API_URL = "http://127.0.0.1:8000"


def calculate_ahp(matrix):

    res = requests.post(
        f"{API_URL}/ahp/calculate",
        json={"matrix": matrix}
    )

    return res.json()


def search_rentals(query, weights):

    res = requests.post(
        f"{API_URL}/rentals/search",
        json={
            "query": query,
            "max_price": 5000000,
            "min_area": 20,
            "weights": weights
        }
    )

    return res.json()