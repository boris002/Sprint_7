import requests
import pytest
import allure
from data.urls import BASE_URL, CREATE_COURIER
from utils import register_new_courier_and_return_login_password
from data.payloads import new_courier_payload

@allure.epic('Courier - Создание курьера')
class TestCourierCreation:

    @allure.title('Создание нового курьера')
    @allure.description(
        'Тест проверяет успешное создание нового курьера с валидными данными через register_new_courier_and_return_login_password. '
        'Ожидается, что вернётся непустой список с логином, паролем и именем.'
    )
    def test_create_courier_success(self):
        login_pass = register_new_courier_and_return_login_password()
        assert login_pass, "Регистрация курьера не удалась, список пустой"
        assert len(login_pass) == 3, f"Ожидался список с 3 элементами, получили {login_pass}"

    @allure.title('Создание курьера с дублирующими данными (ожидается 409)')
    @allure.description(
        'Тест проверяет, что при попытке создать курьера с уже существующим логином API возвращает ошибку 409.'
    )
    def test_create_courier_duplicate_data_returns_409(self):
        login_pass = register_new_courier_and_return_login_password()
        assert login_pass, "Регистрация курьера не удалась"
        
        payload = {
            "login": login_pass[0],
            "password": login_pass[1],
            "firstName": login_pass[2]
        }
        
        response = requests.post(f"{BASE_URL}{CREATE_COURIER}", json=payload)
        assert response.status_code == 409, f"Ожидали 409, получили {response.status_code}"
        body = response.json()
        assert "message" in body
        assert "логин" in body["message"].lower()

    @allure.title('Создание курьера без обязательных полей')
    @allure.description(
        'Тест проверяет поведение API при создании курьера с отсутствующими обязательными полями. '
        'Для login и password ожидается 400 ошибка с сообщением о недостаточных данных, '
        'для firstName курьер создается успешно.'
    )
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field_returns_expected_status(self, missing_field):
        payload = new_courier_payload()
        payload.pop(missing_field)
        response = requests.post(f"{BASE_URL}{CREATE_COURIER}", json=payload)

        if missing_field in ("login", "password"):
            assert response.status_code == 400
            body = response.json()
            assert "message" in body
            assert "недостаточно" in body["message"].lower()
        else:
            assert response.status_code == 201
            assert response.json() == {"ok": True}
