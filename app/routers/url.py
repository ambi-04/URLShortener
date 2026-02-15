from fastapi import APIRouter,Depends,HTTPException,Request,Response,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_cache_redis,get_counter_redis
from app.database import get_db_session
from app.schemas import UrlCreate

router = APIRouter(tags=["url shortening and url redirection"])
@router.post(path="/shorten",tags=["url shortening"]):
async def shorten(input_data:UrlCreate,db:AsyncSession=Depends(get_db_session),counter_redis:AsyncSession=Depends(get_counter_redis)):
