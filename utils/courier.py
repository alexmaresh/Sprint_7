import requests
import random
import string
import allure
from routes import ScooterRoutes as r


class Courier:
    def __init__(self):
        self.data = None
        self.courier_id = None
        self.created_courier = False

    @staticmethod
    @allure.step("Генерация рандомной строки")
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = "".join(random.choice(letters) for i in range(length))
        return random_string

    @allure.step("Генерация данных курьера")
    def generate_courier_data(self):
        payload = {
            "login": self.generate_random_string(10),
            "password": self.generate_random_string(10),
            "firstName": self.generate_random_string(10),
        }
        self.data = payload
        return payload

    @allure.step("Создание курьера")
    def create_courier(self):
        data = self.generate_courier_data()
        response = requests.post(r.COURIER, data=data)
        assert response.status_code == 201, response.json()
        self.created_courier = True

    @allure.step("Логин курьера и получение его id")
    def login_courier(self):
        self.create_courier()
        del self.data["firstName"]
        response = requests.post(r.LOGIN, data=self.data)
        assert response.status_code == 200, response.json()
        self.courier_id = response.json().get("id")
        return response.json().get("id")

    @allure.step("Удаление курьера")
    def delete_courier(self):
        response = requests.delete(r.COURIER + f"/{self.courier_id}")
        assert response.status_code == 200 and response.json().get("ok")
