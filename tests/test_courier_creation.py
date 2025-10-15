import requests
import allure
from data.urls import BASE_URL, CREATE_COURIER,LOGIN_COURIER
from data.payloads import new_courier_payload, courier_login_payload

@allure.epic('Courier - Создание курьера')
class TestCourierCreation:

    @allure.title('Создание нового курьера')
    @allure.description(
        'Тест проверяет успешное создание нового курьера с валидными данными через register_new_courier_and_return_login_password. '
        'Ожидается статус 201 и тело ответа {"ok": True}.'
    )
    def test_create_courier_success(self,create_unique_courier):
        login_pass = [create_unique_courier["login"], create_unique_courier["password"]]


        # Логинимся, чтобы получить id для проверки и удаления
        login_response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER}",
            json=courier_login_payload(login_pass[0], login_pass[1])
        )
        assert login_response.status_code == 200
        body = login_response.json()
        assert "id" in body
        assert isinstance(body["id"], int)

    @allure.title('Создание курьера с дублирующими данными (ожидается 409)')
    @allure.description(
        'Тест проверяет, что при попытке создать курьера с уже существующим логином API возвращает ошибку 409.'
    )
    def test_create_courier_duplicate_data_returns_409(self,create_unique_courier):
        payload = create_unique_courier
        

        response = requests.post(f"{BASE_URL}{CREATE_COURIER}", json=payload)
        assert response.status_code == 409
        body = response.json()
        assert "message" in body
        assert "логин" in body["message"].lower()

    @allure.title('Создание курьера без login')
    @allure.description('Если не передан login, возвращается ошибка 400.')
    def test_create_courier_missing_login_returns_400(self):
        payload = new_courier_payload()
        payload.pop("login")
        response = requests.post(f"{BASE_URL}{CREATE_COURIER}", json=payload)
        assert response.status_code == 400
        body = response.json()
        assert "message" in body
        assert "недостаточно" in body["message"].lower()

    @allure.title('Создание курьера без password')
    @allure.description('Если не передан password, возвращается ошибка 400.')
    def test_create_courier_missing_password_returns_400(self):
        payload = new_courier_payload()
        payload.pop("password")
        response = requests.post(f"{BASE_URL}{CREATE_COURIER}", json=payload)
        assert response.status_code == 400
        body = response.json()
        assert "message" in body
        assert "недостаточно" in body["message"].lower()

    @allure.title('Создание курьера без firstName')
    @allure.description('Если не передан firstName, курьер создаётся успешно.')
    def test_create_courier_missing_firstname_returns_201(self):
        payload = new_courier_payload()
        payload.pop("firstName")
        response = requests.post(f"{BASE_URL}{CREATE_COURIER}", json=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Логинимся чтобы получить ID и убедиться, что курьер действительно создан
        login_response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER}",
            json=courier_login_payload(payload["login"], payload["password"])
        )
        assert login_response.status_code == 200
        assert "id" in login_response.json()
    #убрал лишний тест(повтор первого)