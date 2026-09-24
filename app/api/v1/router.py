"""Aggregates every v1 router into a single mountable router.

Keeping one aggregation point means ``main.py`` never grows a list of imports
as features are added — each phase registers its router here.
"""

from fastapi import APIRouter

from app.api.v1.routers import health

api_router = APIRouter()
api_router.include_router(health.router)

# Registered in later phases:
#   Phase 2 — reports (anonymous submission), cases (case-code lookup)
#   Phase 3 — auth (moderator login)
#   Phase 4 — moderation (queue, filtering, status updates)
