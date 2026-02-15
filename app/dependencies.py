from fastapi import Request

def get_counter_redis(request:Request):
    return request.app.state.counter_redis
def get_cache_redis(request:Request):
    return request.app.state.cache_redis