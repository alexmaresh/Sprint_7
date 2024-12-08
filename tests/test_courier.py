import requests

from routes import ScooterRoutes as r
import pytest
import allure


@allure.feature("Метод создания курьера")
class TestCourierCreate:
    @allure.title("Успешное создание курьера")
    def test_courier_create_success(self, courier_data):
        resp = requests.post(r.COURIER, data=courier_data)
        assert resp.status_code == 201 and resp.json().get("ok"), resp.json()

    @allure.title("Неуспешное создание курьера с неуникальными логином и паролем ")
    def test_courier_create_non_unique_failed(self, courier_data):
        data = courier_data
        resp = requests.post(r.COURIER, data=data)
        assert resp.status_code == 201
        resp = requests.post(r.COURIER, data=data)
        assert (
            resp.status_code == 409
            and resp.json().get("message")
            == "Этот логин уже используется. Попробуйте другой."
        ), resp.json()

    @allure.title("Неуспешное создание курьера с пустым логином и паролем")
    @pytest.mark.parametrize("field", ["login", "password"])
    def test_courier_create_empty_field_failed(self, courier_data, field):
        courier_data[field] = ""
        resp = requests.post(r.COURIER, data=courier_data)
        assert (
            resp.status_code == 400
            and resp.json().get("message")
            == "Недостаточно данных для создания учетной записи"
        ), resp.json()


@allure.feature("Метод логина курьера")
class TestCourierLogin:
    @allure.title("Успешный логин курьера")
    def test_courier_login_success(self, courier_data):
        data = courier_data
        requests.post(r.COURIER, data=courier_data)
        del data["firstName"]
        resp = requests.post(r.LOGIN, data=data)
        assert resp.status_code == 200 and resp.json().get("id")

    @allure.title("Неуспешный логин курьера с несуществующей парой логин-пароль")
    def test_courier_nonexistent_login_fail(self, courier_data):
        resp = requests.post(r.LOGIN, data=courier_data)
        assert (
            resp.status_code == 404
            and resp.json().get("message") == "Учетная запись не найдена"
        )

    @allure.title("Неуспешный логин курьера без логина или пароля")
    @pytest.mark.parametrize("field", ["login", "password"])
    def test_courier_empty_field_fail(self, courier_data, field):
        requests.post(r.COURIER, data=courier_data)
        courier_data[field] = ""
        resp = requests.post(r.LOGIN, data=courier_data)
        assert (
            resp.status_code == 400
            and resp.json().get("message") == "Недостаточно данных для входа"
        )


@allure.feature("Метод удаления курьера")
class TestCourierDelete:
    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self, get_courier_id):
        resp = requests.delete(r.COURIER + f"/{get_courier_id}")
        assert resp.status_code == 200 and resp.json().get("ok")

    @allure.title("Неуспешное удаление курьера с несуществующим id")
    def test_delete_courier_fail(self):
        resp = requests.delete(r.COURIER + "/0")
        assert (
            resp.status_code == 404
            and resp.json().get("message") == "Курьера с таким id нет."
        )

    # Ожидаем тут 400, получаем 500 - песочница не обрабатывает или тут задумано что-то другое в условии?
    @allure.title("Неуспешное удаление курьера без id")
    def test_delete_courier_id_fail(self):
        empty_id = None
        resp = requests.delete(r.COURIER + f"{empty_id}")
        assert (
            resp.status_code == 400
            and resp.json().get("message") == "Недостаточно данных для удаления курьера"
        )
