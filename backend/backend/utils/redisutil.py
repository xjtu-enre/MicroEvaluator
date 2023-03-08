#!/usr/bin/env python
import time

import redis
from redis.exceptions import ConnectionError as RedisConnectionError


class VodRedis(redis.Redis):
    reconnect_timer = 10  # second
    connection_down_timestamp = 0

    def execute_command(self, *args, **options):
        try:
            ok_time = time.time() - (self.connection_down_timestamp + self.reconnect_timer)
            if ok_time > 0:
                self.connection_down_timestamp = 0
                return super(VodRedis, self).execute_command(*args, **options)
            return None
        except RedisConnectionError:
            self.connection_down_timestamp = time.time()
            return None


def redis_pool(db):
    return redis.ConnectionPool(host='127.0.0.1', port='6379', db=db, socket_timeout=5)


default_pool = redis_pool(0)
redis_session = VodRedis(connection_pool=default_pool)


def create_redis_session():
    return redis_session