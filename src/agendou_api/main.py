from contextlib import asynccontextmanager

from fastapi import FastAPI

import agendou_api.companies.infrastructure.persistence.models  # noqa: F401
from agendou_api.companies.infrastructure.http.routes.company_routes import (
    router as companies_router,
)
from agendou_api.shared.infrastructure.database.session import (
    create_async_engine_from_settings,
    dispose_async_engine,
)
from agendou_api.users.infrastructure.http.routes.auth_routes import router as auth_router
from agendou_api.users.infrastructure.http.routes.me_routes import router as me_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_async_engine_from_settings()
    yield
    await dispose_async_engine()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(me_router)
app.include_router(companies_router)


@app.get("/")
def read_root():
    return {"message": "Olá, FastAPI com Poetry!"}


def run() -> None:
    import uvicorn

    uvicorn.run("agendou_api.main:app", host="0.0.0.0", port=8000, reload=True)
