import requests
import pytest
import allure
from data.urls import BASE_URL, LOGIN_COURIER
from data.payloads import courier_login_payload

@allure.epic('Courier - Логин курьера в системе')
class TestCourierLogin:

    @allure.title('Авторизация курьера — успешный вход')
    @allure.description(
        'Тест проверяет, что курьер с валидными учетными данными может успешно войти в систему. '
        'Ожидается статус 200 и наличие ключа "id" в ответе.'
    )
    def test_login_courier_valid_credentials_returns_200_and_id(self, create_unique_courier):
        payload = courier_login_payload(
            create_unique_courier["login"],
            create_unique_courier["password"]
        )
        response = requests.post(f"{BASE_URL}{LOGIN_COURIER}", json=payload)
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Ответ: {response.text}"
        body = response.json()
        assert "id" in body, f"Ожидали ключ 'id' в ответе, получили: {body}"

    @allure.title('Авторизация с неверными учётными данными')
    @allure.description(
        'Тест проверяет, что при попытке авторизации с неверным логином или паролем API возвращает ошибку 404 '
        'с соответствующим сообщением.'
    )
    def test_login_courier_invalid_credentials_returns_404(self):
        payload = {"login": "wronglogin", "password": "wrongpass"}
        response = requests.post(f"{BASE_URL}{LOGIN_COURIER}", json=payload)
        assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}. Ответ: {response.text}"
        body = response.json()
        assert "message" in body
        assert body["message"] in ["Учетная запись не найдена", "Недостаточно данных для входа"]

    @allure.title('Авторизация с пустыми обязательными полями')
    @allure.description(
        'Тест проверяет поведение API при авторизации курьера с пустыми обязательными полями (login или password). '
        'Ожидается ошибка 400 с сообщением о недостаточных данных.'
    )
    @pytest.mark.parametrize("empty_field", ["login", "password"])
    def test_login_courier_empty_field_returns_400(self, create_unique_courier, empty_field):
        payload = {
            "login": create_unique_courier["login"],
            "password": create_unique_courier["password"]
        }

        payload[empty_field] = ""

        response = requests.post(f"{BASE_URL}{LOGIN_COURIER}", json=payload)
        print(f"\nОтвет сервера (пустое поле {empty_field}): {response.status_code} -> {response.text}")

        assert response.status_code == 400, (
            f"Ожидали 400 при пустом поле '{empty_field}', "
            f"получили {response.status_code}. Ответ: {response.text}"
        )

        assert "Недостаточно данных" in response.text, (
            f"Ожидали сообщение об ошибке при пустом поле '{empty_field}', "
            f"получили: {response.text}"
        )
    @allure.title('Получение ID созданного курьера')
    @allure.description(
        'Тест логинит курьера через фикстуру create_unique_courier и проверяет, что в ответе есть ключ "id". '
        'Возвращает id курьера.'
    )
    def test_get_courier_id(self, create_unique_courier):
        payload = courier_login_payload(
            create_unique_courier["login"],
            create_unique_courier["password"]
        )
        response = requests.post(f"{BASE_URL}{LOGIN_COURIER}", json=payload)
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Ответ: {response.text}"
        body = response.json()
        assert "id" in body, f"Ожидали ключ 'id' в ответе, получили: {body}"
        
        courier_id = body["id"]
        print(f"ID созданного курьера: {courier_id}")
        return courier_id
