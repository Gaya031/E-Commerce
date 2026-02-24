from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.api_v1 import api_router
from app.db.redis import init_redis, close_redis
from app.db.postgres import init_db
from app.core.exceptions import AppException
from app.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting RushCart backend...")
    await init_db()
    logger.info("Database schema initialized")
    await init_redis()
    logger.info("Redis connected")
    yield
    logger.info("Shutting down RushCart backend...")
    await close_redis()
    logger.info("Redis connection closed")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                },
            },
            headers={
                "Access-Control-Allow_Origin": "http://localhost:5173",
                "Access-Control-Allow-Credentials": "true"
            },
        )

    return app


app = create_app()
