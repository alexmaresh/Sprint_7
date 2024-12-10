import json

import pytest
from utils.courier import Courier
from utils.order import Order


@pytest.fixture()
def courier_data():
    courier = Courier()
    courier_data = courier.generate_courier_data()
    yield courier_data
    if courier.created_courier:
        courier.login_courier()
        courier.delete_courier()


@pytest.fixture()
def order_data(color):
    order = Order()
    data = order.generate_order_data(color)
    data_j = json.dumps(data)
    yield data_j


@pytest.fixture()
def get_courier_id():
    courier = Courier()
    courier_id = courier.login_courier()
    yield courier_id


@pytest.fixture()
def get_order_id():
    order = Order()
    order.create_order()
    track_id = order.get_track_id()
    yield track_id
