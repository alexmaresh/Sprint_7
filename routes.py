class ScooterRoutes:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/"
    API_URL = BASE_URL + "api/v1/"
    COURIER = API_URL + "courier/"
    LOGIN = COURIER + "login/"
    ORDER = API_URL + "orders/"
    ORDER_ACCEPTED = ORDER + "accept/"
    TRACK = ORDER + "track/"
