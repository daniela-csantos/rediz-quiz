import redis

class Config:
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0

def get_redis_client():
    return redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB, decode_responses=True)
