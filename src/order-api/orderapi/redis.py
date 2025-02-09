import redis


class RedisUtil:
    def __init__(self, addr, port, db):
        self.addr = addr
        self.port = port
        self.cache_db = db

    def _get_client(self):
        return redis.Redis(self.addr, self.port, self.cache_db)

    def get(self, key):
        r = self._get_client()
        return r.get(key)

    def set(self, key, value):
        r = self._get_client()
        r.set(key, value)
