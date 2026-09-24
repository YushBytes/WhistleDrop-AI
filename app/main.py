"""Application entry point.

Uses the application-factory pattern: ``create_app()`` builds a fully wired
FastAPI instance from a ``Settings`` object. Tests can therefore construct an
app with test configuration instead of mutating global state, and the module
stays free of import-time side effects beyond the default instance below.
"""

from fastapi import FastAPI

from app import __version__
from app.api.v1.router import api_router
from app.core.config import Settings, get_settings

API_DESCRIPTION = """
**WhistleDrop AI** is a confidential reporting backend. Reports are submitted
without an account and without any identifying information. Each submission
returns a single-use **case code** that is the only way to track the report.

### Anonymity — what this system does and does not guarantee

* No reporter name, email, phone number or account is ever collected or stored.
* The case code is stored only as a keyed hash, never in plaintext.
* Network-level anonymity is **out of scope**. Use Tor or a VPN if your threat
  model requires it.
* A report can still de-anonymise its author through its own contents.

### AI-assisted triage

AI triage is an **extension** to the official task specification, not part of
it. Its output is advisory only: it can never change a report's status or its
official category. A moderator always decides.
"""


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure a FastAPI application instance."""
    settings = settings or get_settings()

    app = FastAPI(
        title=settings.app_name,
        description=API_DESCRIPTION,
        version=__version__,
        docs_url="/docs" if settings.enable_docs else None,
        redoc_url="/redoc" if settings.enable_docs else None,
        openapi_url="/openapi.json" if settings.enable_docs else None,
        contact={"name": "WhistleDrop AI", "url": "https://github.com/YushBytes"},
        license_info={"name": "MIT"},
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
