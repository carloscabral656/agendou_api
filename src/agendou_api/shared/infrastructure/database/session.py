from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from agendou_api.config.settings import Settings, get_settings

_engine = None
_async_session_maker: async_sessionmaker[AsyncSession] | None = None


def create_async_engine_from_settings(settings: Settings | None = None):
    global _engine, _async_session_maker
    settings = settings or get_settings()
    _engine = create_async_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
    )
    _async_session_maker = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    return _engine


def get_async_session_maker() -> async_sessionmaker[AsyncSession]:
    if _async_session_maker is None:
        create_async_engine_from_settings()
    assert _async_session_maker is not None
    return _async_session_maker


async def get_async_session() -> AsyncIterator[AsyncSession]:
    maker = get_async_session_maker()
    async with maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def dispose_async_engine() -> None:
    global _engine, _async_session_maker
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _async_session_maker = None
