import requests
from routes import ScooterRoutes as r
import pytest
import allure


@allure.feature("Метод создания заказа")
class TestOrderCreate:
    @allure.title("Успешное создание заказа с разными цветами самокатов")
    @pytest.mark.parametrize("color", (["BLACK"], ["GREY"], ["BLACK", "GREY"], ""))
    def test_order_create(self, order_data, color):
        resp = requests.post(r.ORDER, data=order_data)
        assert resp.status_code == 201 and resp.json().get("track")


@allure.feature("Метод получения списка заказов")
class TestListOrders:
    @allure.title("Успешное получение списка заказов")
    def test_list_orders(self):
        resp = requests.get(r.ORDER)
        assert resp.status_code == 200, resp.json()


@allure.feature("Метод принятия заказа")
class TestOrderAccepted:
    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self, get_order_id, get_courier_id):
        order_id = get_order_id
        courier_id = get_courier_id
        url = r.ORDER_ACCEPTED + f"{order_id}?courierId={courier_id}"
        resp = requests.put(url)
        assert resp.status_code == 200 and resp.json().get("ok"), resp.json()

    @allure.title("Неуспешное принятие заказа без id курьера")
    def test_accept_order_no_id_courier_fail(self, get_order_id):
        url = r.ORDER_ACCEPTED + f"{get_order_id}"
        resp = requests.put(url)
        assert (
            resp.status_code == 400
            and resp.json().get("message") == "Недостаточно данных для поиска"
        ), resp.json()

    @allure.title("Неуспешное принятие заказа без id заказа")
    def test_accept_order_no_id_order_fail(self, get_courier_id):
        url = r.ORDER_ACCEPTED + f"courierId={get_courier_id}"
        resp = requests.put(url)
        assert (
            resp.status_code == 400
            and resp.json().get("message") == "Недостаточно данных для поиска"
        ), resp.json()

    @allure.title("Неуспешное принятие заказа с некорректным номером заказа")
    def test_accept_order_incorrect_order_fail(self, get_courier_id):
        url = r.ORDER_ACCEPTED + f"0?courierId={get_courier_id}"
        resp = requests.put(url)
        assert (
            resp.status_code == 404
            and resp.json().get("message") == "Заказа с таким id не существует"
        ), resp.json()

    @allure.title("Неуспешное принятие заказа с некорректным номером курьера")
    def test_accept_order_incorrect_courier_fail(self, get_order_id, get_courier_id):
        url = r.ORDER_ACCEPTED + f"{get_order_id}?courierId=0"
        resp = requests.put(url)
        assert (
            resp.status_code == 404
            and resp.json().get("message") == "Курьера с таким id не существует"
        ), resp.json()


@allure.feature("Метод получения информации о заказе по трек-номеру")
class TestOrderGet:
    @allure.title("Успешное получение инфы о заказе по корректному трек-номеру")
    def test_get_order_by_number(self, get_order_id):
        params = {"t": get_order_id}
        resp = requests.get(r.TRACK, params=params)
        assert resp.status_code == 200 and resp.json().get("order"), resp.json()

    @allure.title("Неуспешное получение инфы о заказе без трек-номера")
    def test_get_order_fail(self):
        resp = requests.get(r.TRACK)
        assert (
            resp.status_code == 400
            and resp.json().get("message") == "Недостаточно данных для поиска"
        ), resp.json()

    @allure.title("Неуспешное получение инфы о заказе по некорректному трек-номеру")
    def test_get_order_wrong_fail(self):
        params = {"t": 0}
        resp = requests.get(r.TRACK, params=params)
        assert (
            resp.status_code == 404 and resp.json().get("message") == "Заказ не найден"
        ), resp.json()
