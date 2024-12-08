import json
import allure
from faker import Faker
import requests
import random
from routes import ScooterRoutes as r


class Order:
    def __init__(self):
        self.track_id = None

    @staticmethod
    @allure.step("Генерация данных заказа")
    def generate_order_data(color):
        fake = Faker()

        params = {
            "name": fake.first_name(),
            "lastName": fake.last_name(),
            "address": fake.address(),
            "metroStation": random.randint(1, 30),
            "phone": fake.phone_number(),
            "rentTime": random.randint(1, 7),
            "deliveryDate": fake.date_between(
                start_date="today", end_date="+2y"
            ).strftime("%Y-%m-%d"),
            "comment": fake.sentence(),
            "color": color,
        }
        return params

    @allure.step("Создание заказа")
    def create_order(self):
        color = ["BLACK"]
        params = self.generate_order_data(color)
        resp = requests.post(r.ORDER, data=json.dumps(params))
        assert resp.status_code == 201 and resp.json().get("track"), resp.json()
        self.track_id = resp.json()["track"]

    @allure.step("Вернуть номер заказа, проверив что он существует")
    def get_track_id(self):
        params = {"t": self.track_id}
        resp = requests.get(r.TRACK, params=params)
        assert resp.status_code == 200 and resp.json().get("order"), resp.json()
        return self.track_id
