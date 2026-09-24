"""Shared pytest fixtures.

Tests never read the developer's ``.env``. Settings are constructed explicitly
and injected through ``app.dependency_overrides`` so that a test run cannot be
influenced by — or accidentally act on — local configuration.
"""

from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import create_app


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Settings used by the whole test session."""
    return Settings(
        app_env="test",
        debug=True,
        enable_docs=True,
        # Phase 1 replaces this with the real test-container DSN from
        # TEST_DATABASE_URL. Nothing connects to a database yet.
        database_url="postgresql+psycopg://test:test@localhost:5433/whistledrop_test",
    )


@pytest.fixture(scope="session")
def app(test_settings: Settings) -> FastAPI:
    """A FastAPI app wired with test settings."""
    application = create_app(test_settings)
    application.dependency_overrides[get_settings] = lambda: test_settings
    return application


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    """HTTP client bound to the test application."""
    with TestClient(app) as test_client:
        yield test_client
