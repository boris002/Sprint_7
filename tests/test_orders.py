import requests
import pytest
from data.urls import BASE_URL, ORDERS_LIST
from data.payloads import order_payload
import allure

@allure.epic('Orders - Создание заказа')
class TestOrders:

    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], None])
    @allure.title('Создание заказа')
    @allure.description(
        'Тест проверяет создание заказа с разными цветами. Ожидается статус 201 и наличие ключа "track" в ответе.'
    )
    def test_create_order_with_color_returns_201_and_track(self, color):
        payload = order_payload(color)
        response = requests.post(f"{BASE_URL}{ORDERS_LIST}", json=payload, timeout=10)
        
        assert response.status_code == 201, (
            f"Ожидали 201 при создании заказа с цветом {color}, получили {response.status_code}. Ответ: {response.text}"
        )
        body = response.json()
        assert "track" in body, f"Ожидали ключ 'track' в ответе при цвете {color}, получили: {body}"
