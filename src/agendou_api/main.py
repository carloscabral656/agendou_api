from contextlib import asynccontextmanager

from fastapi import FastAPI

from agendou_api.shared.infrastructure.database.session import (
    create_async_engine_from_settings,
    dispose_async_engine,
)
from agendou_api.users.infrastructure.http.routes.user_routes import router as users_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_async_engine_from_settings()
    yield
    await dispose_async_engine()


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)


@app.get("/")
def read_root():
    return {"message": "Olá, FastAPI com Poetry!"}


def run() -> None:
    import uvicorn

    uvicorn.run("agendou_api.main:app", host="0.0.0.0", port=8000, reload=True)
