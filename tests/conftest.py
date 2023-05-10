"""
Global test fixtures
"""
from typing import Iterator

import pytest
from cachelib.simple import SimpleCache
from dj.api.main import app
from dj.config import Settings
from dj.utils import get_session, get_settings
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool


@pytest.fixture
def settings(mocker: MockerFixture) -> Iterator[Settings]:
    """
    Server settings for testing
    """
    settings = Settings(
        index="sqlite://",
        repository="/path/to/repository",
        results_backend=SimpleCache(default_timeout=0),
        celery_broker=None,
        redis_cache=None,
        query_service=None,
    )

    mocker.patch(
        "dj.utils.get_settings",
        return_value=settings,
    )

    yield settings


@pytest.fixture
def session() -> Iterator[Session]:
    """
    SQLite database session for testing
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine, autoflush=False) as session:
        yield session


@pytest.fixture
def client(
    session: Session,
    settings: Settings,
) -> Iterator[TestClient]:
    """
    API Client for testing
    """

    def get_session_override() -> Session:
        return session

    def get_settings_override() -> Settings:
        return settings

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
