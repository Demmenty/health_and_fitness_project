from fatsecret_app.services import FatsecretManager


class Services:
    def __init__(self):
        self.fs = FatsecretManager()


services = Services()
