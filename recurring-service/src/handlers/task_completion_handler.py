# [Task]: T092
# [Spec]: F-010 (R-010.1, R-010.2)
# [Description]: Task completion event handler for recurring service
"""
Task completion event handler.
Processes task completion events and creates next recurring task occurrences.
"""
import logging
from typing import Dict, Any
from datetime import datetime, timezone, timedelta
from uuid import UUID

from ..services.recurring_service import RecurringService

logger = logging.getLogger(__name__)


class TaskCompletionHandler:
    """
    Handles task completion events from the task service.

    Processes task completion events received via Dapr pub/sub and
    creates the next occurrence for recurring tasks.
    """

    def __init__(self):
        self.recurring_service = RecurringService()

    async def handle_task_completion_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a task completion event from the task service.

        Args:
            event_data: The task completion event data from Dapr pub/sub

        Returns:
            Dict containing processing result
        """
        try:
            logger.info(f"Received task completion event: {event_data}")

            # Validate event data
            if not self._validate_event_data(event_data):
                return {
                    "status": "error",
                    "message": "Invalid task completion event data"
                }

            # Extract event details
            task_id = event_data.get("task_id")
            user_id = event_data.get("user_id")
            recurrence = event_data.get("recurrence")

            logger.info(f"Processing completion of task {task_id} for user {user_id}")

            # Check if task is recurring
            if not recurrence or recurrence == "none":
                logger.info(f"Task {task_id} is not recurring, no further action needed")
                return {
                    "status": "success",
                    "message": "Task is not recurring",
                    "task_id": task_id
                }

            # Create next recurring task occurrence
            next_task_result = await self.recurring_service.create_next_recurring_task(
                task_id=task_id,
                user_id=user_id,
                recurrence=recurrence
            )

            if next_task_result["success"]:
                logger.info(f"Successfully created next recurring task for {task_id}")
                return {
                    "status": "success",
                    "message": f"Next recurring task created: {next_task_result['next_task_id']}",
                    "task_id": task_id,
                    "next_task_id": next_task_result["next_task_id"]
                }
            else:
                logger.error(f"Failed to create next recurring task for {task_id}: {next_task_result['message']}")
                return {
                    "status": "error",
                    "message": f"Failed to create next task: {next_task_result['message']}",
                    "task_id": task_id
                }

        except Exception as e:
            logger.error(f"Unexpected error handling task completion event: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }

    def _validate_event_data(self, event_data: Dict[str, Any]) -> bool:
        """
        Validate the task completion event data.

        Args:
            event_data: The event data to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["task_id", "user_id"]
        for field in required_fields:
            if field not in event_data or not event_data[field]:
                logger.warning(f"Missing required field: {field}")
                return False

        return True


# Singleton instance
task_completion_handler = TaskCompletionHandler()
