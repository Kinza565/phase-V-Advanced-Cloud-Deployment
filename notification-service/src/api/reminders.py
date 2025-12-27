# [Task]: T091
# [Spec]: F-009 (R-009.1)
# [Description]: Reminder API endpoints for notification service
"""
Reminder API endpoints.
Handles reminder events from Dapr pub/sub.
"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any

from ..handlers.reminder_handler import reminder_handler

router = APIRouter()


class ReminderEvent(BaseModel):
    """Reminder event model for Dapr pub/sub."""
    task_id: str
    title: str
    due_at: str = None
    remind_at: str = None
    user_id: str


@router.post(
    "/handle",
    status_code=status.HTTP_200_OK,
    summary="Handle reminder event",
    description="Process reminder events from Dapr pub/sub"
)
async def handle_reminder_event(request: Request) -> Dict[str, Any]:
    """
    Handle reminder events from Dapr pub/sub.

    This endpoint receives reminder events from the task service
    and processes them to send notifications to users.
    """
    try:
        # Get the raw event data from Dapr
        event_data = await request.json()

        # Handle the reminder event
        result = await reminder_handler.handle_reminder_event(event_data)

        # Return appropriate response based on result
        if result.get("status") == "success":
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=result
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=result
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": f"Failed to process reminder event: {str(e)}"
            }
        )
