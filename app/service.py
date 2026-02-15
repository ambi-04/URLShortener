from dotenv import load_dotenv
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import get_cached_url,get_longurl_db,get_unique_id,create_url,insert_cache
import os

load_dotenv()
domain_url = os.getenv("DOMAIN_URL")
def encode_base62(num:int):
    base62digits = "0123456789ABCDEFGHIJabcdefghijklmnopqrstuvwxyz"
    encoded_string_list = []
    while num > 0:
        char = base62digits[num % 62]
        encoded_string_list.insert(0, char)
        num = num / 62
    while len(encoded_string_list) < 7:
        encoded_string_list.insert(0,'0')
    encoded_string = str(list)
    return encoded_string

async def shorten_service(longurl:str, db:AsyncSession, counter_redis:Redis):
    id_generated = await (get_unique_id(counter_redis))
    shorturl = domain_url + "/" + encode_base62(id_generated)
    create_url(longurl,shorturl,db)
    return shorturl

async def redirection_service(shorturl:str, db: AsyncSession, cache_redis:Redis):
    longurl = await get_cached_url(shorturl,cache_redis)
    if longurl is None:
        longurl = await get_longurl_db(shorturl,db)
        if longurl is None:
            return "invalid longurl"
        await insert_cache(shorturl,longurl,cache_redis)
    return  longurl

