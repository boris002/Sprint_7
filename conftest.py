import pytest
from utils import register_new_courier_and_return_login_password
from data.urls import BASE_URL, CREATE_COURIER
import requests


@pytest.fixture
def create_unique_courier():
    login_pass = register_new_courier_and_return_login_password()
    if not login_pass:
        pytest.fail("Не удалось зарегистрировать нового курьера через register_new_courier_and_return_login_password")
    return {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }
@pytest.fixture
def delete_courier():
    def _delete(courier_id):
        requests.delete(f"{BASE_URL}{CREATE_COURIER}{courier_id}", json={"id": str(courier_id)})
    return _delete