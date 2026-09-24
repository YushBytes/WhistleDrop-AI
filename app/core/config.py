"""Application configuration.

Every environment-specific or secret value is read from the environment (or a
local ``.env`` file) rather than being written into the source tree. This keeps
credentials out of version control and lets the same image run in development,
test and production with different configuration.

See ``.env.example`` for the full list of supported variables.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["development", "test", "production"]


class Settings(BaseSettings):
    """Typed, validated application settings.

    Values are loaded from environment variables first and from ``.env``
    second. Field names map to upper-case variable names, so ``app_name``
    is read from ``APP_NAME``.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # docker-compose reads POSTGRES_* from the same .env file; those are not
        # application settings, so unknown keys are ignored rather than fatal.
        extra="ignore",
    )

    # --- Application -------------------------------------------------------
    app_name: str = "WhistleDrop AI"
    app_env: Environment = "development"
    debug: bool = False
    log_level: str = "INFO"

    api_v1_prefix: str = "/api/v1"

    # The GDG task requires the API to be demonstrable through Swagger, so the
    # interactive docs are enabled by default. A hardened deployment of a real
    # whistleblowing service would gate this behind authentication.
    enable_docs: bool = True

    # --- Database ----------------------------------------------------------
    # Required with no default: the application must fail loudly at startup if
    # it was deployed without a database, rather than silently falling back to
    # something unexpected. Unused until Phase 1.
    database_url: str = Field(
        ...,
        description="SQLAlchemy DSN for the application database.",
    )

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings.

    Cached so that the ``.env`` file is parsed once per process. Used as a
    FastAPI dependency, which also makes it straightforward to override with
    test settings via ``app.dependency_overrides``.
    """
    return Settings()  # type: ignore[call-arg]  # values come from the environment
