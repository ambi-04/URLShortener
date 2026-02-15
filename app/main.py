
from fastapi import FastAPI, HTTPException, Request
from .routers import admin_user_management,admin,auth,admin_ef_search,standards_basic_advanced_users,ef_search_basic_advanced_user_API,ef_versions_basic_advanced_users,admin_update_ef,admin_get_ef_logs
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# --- Imports for database tables ---
from app.database import async_engine, Base
from app.models import * # Makes sure all models are loaded
import redis.asyncio as redis
# ------------------------------------


# Async function to create tables
async def create_db_tables():
    async with async_engine.begin() as conn:
        # This line creates all tables defined in your models
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup, create the database tables
    print("Server starting up...")
    await create_db_tables()
    print("Database tables created.")
    # Counter Redis (durable)
    app.state.counter_redis = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

    # Cache Redis (LRU)
    app.state.cache_redis = redis.Redis(
        host="localhost",
        port=6380,
        decode_responses=True
    )
    yield
    # On shutdown
    print("Server shutting down...")
    await (app.state.counter_redis.close())
    await (app.state.cache_redis.close())


app = FastAPI(title="EF Search API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Your Next.js app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    message = ""
    if exc.status_code == 400:
        message = "Bad Request — Invalid input or parameters"
    elif exc.status_code == 403:
        message = "Forbidden — You don’t have permission"
    elif exc.status_code == 404:
        message = "Not Found — Resource does not exist"
    elif exc.status_code == 422:
        message = "Unprocessable entity"
    return JSONResponse(
        status_code=exc.status_code,
        content=
        {
            "success" : False,
            "message": message,
            "error": exc.detail,
            "path" : str(request.url)
        }
    )
# Include your routers
app.include_router(auth.router)
app.include_router(admin_get_ef_logs.router)
app.include_router(admin_user_management.router)
app.include_router(admin_update_ef.router)
app.include_router(admin.router)
app.include_router(admin_ef_search.router)
app.include_router(admin_add_ef.router)
app.include_router(standards_basic_advanced_users.router)
app.include_router(ef_search_basic_advanced_user_API.router)
app.include_router(ef_versions_basic_advanced_users.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the ambiiURL"}