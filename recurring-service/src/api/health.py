# [Task]: T003
# [Spec]: F-010 (R-010.1)
# [Description]: Health check API endpoints for recurring service
"""
Health check API endpoints.
Provides health status for the recurring service.
"""
from fastapi import APIRouter

from ..core.config import settings

router = APIRouter()


@router.get(
    "/",
    summary="Health check",
    description="Returns the health status of the recurring service"
)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }


@router.get(
    "/detailed",
    summary="Detailed health check",
    description="Returns detailed health information including configuration"
)
async def detailed_health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "dapr_http_port": settings.dapr_http_port,
        "pubsub_name": settings.pubsub_name,
        "log_level": settings.log_level,
        "log_json": settings.log_json
    }
