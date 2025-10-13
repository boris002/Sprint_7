import random
import string

def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def new_courier_payload():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }

def courier_login_payload(login, password):
    return {
        "login": login,
        "password": password
    }

def order_payload(color=None):
    payload = {
        "firstName": "John",
        "lastName": "Doe",
        "address": "123 Main St",
        "metroStation": 4,
        "phone": "+70000000000",
        "rentTime": 5,
        "deliveryDate": "2025-10-15",
        "comment": "Test order"
    }
    if color:
        payload["color"] = color
    return payload
