from fatsecret_app.cache_manager import FatsecretCacheManager


class CacheManager():
    def __init__(self):
        self.fs = FatsecretCacheManager()


cache = CacheManager()
