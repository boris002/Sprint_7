# Sprint_7
Файлы тестов:
test_courier_creation.py
Тесты проверки создания курьера: успешное создание, дублирование, отсутствие обязательных полей.
test_courier_login.py
Тесты логина курьера: успешная авторизация, неверные данные, пустые поля.
test_orders_list.py
Тест получения списка заказов: проверка статуса и наличия ключа "orders".
test_orders.py
Тест создания заказа: проверка разных цветов заказаю

urls.py - содержит url страниц

payloads.py
Содержит функции для генерации payload для курьера и заказа: случайный логин, пароль, имя курьера, данные для логина и создания заказа с цветами.
utils.py
Содержит метод register_new_courier_and_return_login_password(), который регистрирует нового курьера через API и возвращает список [login, password, firstName].
conftest.py
Содержит фикстуру create_unique_courier, которая создаёт курьера через метод из utils.py и возвращает словарь с логином, паролем и именем для использования в тестах.

Courier - Создание курьера
test_create_courier_valid_data_returns_201 — проверяет успешное создание нового курьера, ожидается статус 201 и ответ {"ok": True}.
test_create_courier_duplicate_data_returns_409 — проверяет, что при создании курьера с существующим логином возвращается ошибка 409.
test_create_courier_missing_field_returns_expected_status — проверяет создание курьера с пропущенными обязательными полями, для login и password ожидается 400, для firstName — успешное создание.
Courier - Логин курьера
test_login_courier_valid_credentials_returns_200_and_id — проверяет успешную авторизацию курьера, ожидается статус 200 и ключ "id" в ответе.
test_login_courier_invalid_credentials_returns_404 — проверяет авторизацию с неверными данными, ожидается 404 и соответствующее сообщение.
test_login_courier_empty_field_returns_400 — проверяет авторизацию с пустыми обязательными полями, ожидается 400 и сообщение о недостаточных данных.
Orders - Получение списка заказов
test_get_orders_list_returns_200_and_orders — проверяет получение списка заказов, ожидается статус 200 и наличие ключа "orders", который должен быть списком.
Orders - Создание заказа
test_create_order_with_color_returns_201_and_track — проверяет создание заказа с разными цветами, ожидается статус 201 и наличие ключа "track" в ответе.

test_courier_is_created - проверка что курьер создан

test_get_courier_id - id созданного курьера