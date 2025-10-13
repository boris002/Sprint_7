import requests
from data.urls import BASE_URL, ORDERS_LIST
import allure

@allure.epic('Orders - Получение списка заказов')
class TestOrdersList:

    @allure.title('Получение списка заказов')
    @allure.description(
        'Тест проверяет получение списка заказов. Ожидается статус 200 и наличие ключа "orders" в ответе, '
        'который должен быть списком.'
    )
    def test_get_orders_list_returns_200_and_orders(self):
        response = requests.get(f"{BASE_URL}{ORDERS_LIST}", timeout=10)
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Ответ: {response.text}"
        json_data = response.json()
        assert "orders" in json_data, f"В ответе нет ключа 'orders': {json_data}"
        assert isinstance(json_data["orders"], list), f"Ожидали список, получили: {type(json_data['orders'])}"
