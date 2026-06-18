import os
from dotenv import load_dotenv
import redis
from kvsqlite.sync import Client as DB
import requests

load_dotenv(override=True)

import time
import threading

class CachedRedis:
    def __init__(self, real_redis, ttl=5):
        self._r = real_redis
        self._ttl = ttl
        self._cache = {}
        self._lock = threading.Lock()

    def _get_cached(self, cache_key, fetch_fn):
        now = time.time()
        with self._lock:
            if cache_key in self._cache:
                val, expiry = self._cache[cache_key]
                if now < expiry:
                    return val
        val = fetch_fn()
        with self._lock:
            self._cache[cache_key] = (val, now + self._ttl)
        return val

    def _invalidate(self):
        with self._lock:
            self._cache.clear()

    def get(self, key): return self._get_cached(f"get:{key}", lambda: self._r.get(key))
    def hget(self, name, key): return self._get_cached(f"hget:{name}:{key}", lambda: self._r.hget(name, key))
    def hgetall(self, name): return self._get_cached(f"hgetall:{name}", lambda: self._r.hgetall(name))
    def smembers(self, name): return self._get_cached(f"smembers:{name}", lambda: self._r.smembers(name))
    def sismember(self, name, value): return self._get_cached(f"sismember:{name}:{value}", lambda: self._r.sismember(name, value))
    def keys(self, pattern="*"): return self._get_cached(f"keys:{pattern}", lambda: self._r.keys(pattern))
    def ttl(self, name): return self._get_cached(f"ttl:{name}", lambda: self._r.ttl(name))

    def set(self, *args, **kwargs):
        res = self._r.set(*args, **kwargs)
        self._invalidate()
        return res
    def delete(self, *names):
        res = self._r.delete(*names)
        self._invalidate()
        return res
    def sadd(self, name, *values):
        res = self._r.sadd(name, *values)
        self._invalidate()
        return res
    def srem(self, name, *values):
        res = self._r.srem(name, *values)
        self._invalidate()
        return res
    def hset(self, *args, **kwargs):
        res = self._r.hset(*args, **kwargs)
        self._invalidate()
        return res
    def hdel(self, name, *keys):
        res = self._r.hdel(name, *keys)
        self._invalidate()
        return res
    def incr(self, name, amount=1):
        res = self._r.incr(name, amount)
        self._invalidate()
        return res
    def expire(self, name, time):
        res = self._r.expire(name, time)
        self._invalidate()
        return res

    def __getattr__(self, name):
        return getattr(self._r, name)

# Get Redis URL from environment (Render/Cloud) or default to localhost
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
_real_r = redis.from_url(redis_url, decode_responses=True)
r = CachedRedis(_real_r, ttl=5)

token = os.getenv("BOT_TOKEN", "")
IS_FACTORY = os.getenv("IS_FACTORY", "False") == "True"
if not token:
    token = input("[+] Enter the bot token: ")
    with open(".env", "a") as f:
        f.write(f"\nBOT_TOKEN={token}\n")

Dev_Zaid = token.split(':')[0]

# Get sudo ID
owner_id = r.get(f'{Dev_Zaid}botowner')
if not owner_id:
    try:
        owner_id = int(os.getenv("SUDO_ID", "0"))
    except:
        owner_id = 0
    if not owner_id:
        owner_id = int(input("[+] Enter SUDO ID: "))
        with open(".env", "a") as f:
            f.write(f"\nSUDO_ID={owner_id}\n")
    r.set(f'{Dev_Zaid}botowner', owner_id)
else:
    owner_id = int(owner_id)

sudo_id = owner_id

# Fetch bot username dynamically
botUsername = os.getenv("BOT_USERNAME", "")
if not botUsername:
    try:
        req = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()
        if "result" in req:
            botUsername = req["result"]["username"]
            with open(".env", "a") as f:
                f.write(f"\nBOT_USERNAME={botUsername}\n")
    except:
        botUsername = "unknown"

ytdb = DB('ytdb.sqlite')
sounddb = DB('sounddb.sqlite')
wsdb = DB('wsdb.sqlite')
