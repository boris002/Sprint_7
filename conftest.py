import pytest
from utils import register_new_courier_and_return_login_password
from data.urls import BASE_URL, CREATE_COURIER,LOGIN_COURIER
import requests


@pytest.fixture
def create_unique_courier():
    login_pass = register_new_courier_and_return_login_password()
    if not login_pass:
        pytest.fail("Не удалось зарегистрировать нового курьера через register_new_courier_and_return_login_password")
    courier_data = {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }

    yield courier_data

    #удаление курьера после теста 
    login_response = requests.post(
        f"{BASE_URL}{LOGIN_COURIER}",
        json={"login": courier_data["login"], "password": courier_data["password"]}
    )

    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        requests.delete(f"{BASE_URL}{CREATE_COURIER}/{courier_id}")
    
