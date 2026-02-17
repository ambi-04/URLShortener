from fastapi import APIRouter,Depends,HTTPException,Request,Response,status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_cache_redis,get_counter_redis
from app.database import get_db_session
from app.schemas import ShortenUrlInput
import app.service as service

router = APIRouter(tags=["url shortening and url redirection"])
@router.post(path="/shorten",status_code=status.HTTP_201_CREATED)
async def shorten(input_data:ShortenUrlInput,db:AsyncSession=Depends(get_db_session),counter_redis:Redis=Depends(get_counter_redis)):
    shorturl = await service.shorten_service(input_data.longurl,db,counter_redis)
    return {
        "success":True,
        "message":"shorturl created successfully",
        "shorturl":shorturl
    }
@router.get(path="/{shorturl}",status_code=status.HTTP_302_FOUND)
async def redirect(shorturl:str,response:Response,db:AsyncSession=Depends(get_db_session),cache_redis:Redis=Depends(get_cache_redis)):
    longurl = await service.redirection_service(shorturl,db,cache_redis)
    response.headers["Location"] = longurl
    return {
        "success":True,
        "message":"redirected successfully",
        "longurl":longurl
    }