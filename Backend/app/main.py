# import uvicorn
# from fastapi import FastAPI
# from app.core.config import settings
# from .api.api_v1 import api_router
# from app.db.postgres import engine
# from app.db.base import Base
# import asyncio

from fastapi import FastAPI
from app.core.config import settings
from .api.api_v1 import api_router
from app.db.postgres import engine
from sqlalchemy import text
from app.db.base import Base


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)
    app.include_router(api_router, prefix=settings.API_V1_STR)
    return app

app = create_app()

# async def init_models():
#     try:
#         async with engine.begin() as conn:
#             await conn.run_sync(Base.metadata.create_all)
#         print("DB Connected")
#     except Exception as e:
#         print("DB Connection failed")

@app.on_event("startup")
async def startup():
    print("⏳ Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Users & other tables created (if not exist)")
    print("✅ DB Connected")


        
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(init_models())
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    