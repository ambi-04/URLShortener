from pydantic import HttpUrl
from sqlalchemy import select
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import UrlMapper

async def get_unique_id(counter_redis:Redis):
    return await counter_redis.incr("count")

async def get_cached_url(shorturl: str, cache_redis:Redis):
    return await cache_redis.get(shorturl)

async def get_longurl_db(shorturl:str, db: AsyncSession):
    statement = select(UrlMapper.long_url).where(UrlMapper.short_url == shorturl)
    return (await db.scalars(statement)).first()

async def insert_cache(shorturl:str, longurl:str, cache_redis:Redis):
    await cache_redis.set(shorturl, longurl)

def create_url(long_url:str,short_url:str, db: AsyncSession):
    db.add(UrlMapper(long_url = long_url, short_url = short_url))
