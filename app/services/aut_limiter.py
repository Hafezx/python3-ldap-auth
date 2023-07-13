import redis
import config
from app.logger import admin_panel_transaction_logger,ms_error_logger,ms_warning_logger
from app.services.app_exceptions import CustomException,RateLimitException

# redis Singletone connection class
class RedisConn(object):
    _instance = None
    def __init__(self) -> None:
        raise RuntimeError('Call instance() instead')
    
    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = redis.StrictRedis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                db=config.REDIS_DB,
                password=config.REDIS_PASSWORD,
                decode_responses=True
            )
        return cls._instance





# redis connection limiter check
def redis_limiter_check(username)->bool:
    redis_conn = RedisConn.getInstance()

    try:

        if redis_conn.exists(username):
            if int(redis_conn.get(username)) >= int(config.REQUEST_LIMIT):
                ms_warning_logger(
                    response_code=910201,
                    action="REDIS_LIMITER_CHECK",
                    username=username,
                    log_message="user reach limit"
                )
                raise RateLimitException(" خطای تعداد درخواست بیش از حد مجاز لطفا بعدا تلاش کنید")

    except RateLimitException as e:
        raise e
    except Exception as e:
        print(e)
        # just log error
        ms_error_logger(
            response_code=910201,
            action="REDIS_LIMITER_CHECK",
            username=username,
            log_message="redis_limiter_check error:{}".format(e)
        )
        return True


# redis connection limiter increase

def redis_limiter_increase(username)->bool:
    redis_conn = RedisConn.getInstance()

    try:
        if not redis_conn.exists(username):
            redis_conn.set(username,0,ex=convert_to_seconds(config.REQUEST_LIMIT_TIME))
        redis_conn.incr(username)
    except Exception as e:
        # just log error
        ms_error_logger("redis_limiter_increase error:{}".format(e))
    
    return True


seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

def convert_to_seconds(s):
    return int(s[:-1]) * seconds_per_unit[s[-1]]