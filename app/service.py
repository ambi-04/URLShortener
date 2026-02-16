from dotenv import load_dotenv
from fastapi import HTTPException,status
from pydantic import HttpUrl
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import get_cached_url,get_longurl_db,get_unique_id,create_url,insert_cache
import os

load_dotenv()
base_url = os.getenv("API_BASE_URL")
def encode_base62(num:int):
    base62digits = "0123456789ABCDEFGHIJabcdefghijklmnopqrstuvwxyz"
    encoded_string_list = []
    while num > 0:
        char = base62digits[num % 62]
        encoded_string_list.insert(0, char)
        num = num // 62
    while len(encoded_string_list) < 7:
        encoded_string_list.insert(0,'0')
    encoded_string = "".join(encoded_string_list)
    return encoded_string

async def shorten_service(longurl:HttpUrl, db:AsyncSession, counter_redis:Redis):
    try:
        id_generated = await (get_unique_id(counter_redis))
        generated_url = encode_base62(id_generated)
        create_url(str(longurl),generated_url,db)
        await db.commit()
    except Exception as e:
        print(e)
        await db.rollback()
        raise
    shorturl = base_url + "/" + generated_url
    return shorturl

async def redirection_service(shorturl:str, db: AsyncSession, cache_redis:Redis):
    try:
        longurl = await get_cached_url(shorturl,cache_redis)
        if longurl is None:
            longurl = await get_longurl_db(shorturl,db)
            if longurl is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid shorturl")
            await insert_cache(shorturl,longurl,cache_redis)
    except Exception as e:
        print(e)
        await db.rollback()
        raise
    return  longurl

