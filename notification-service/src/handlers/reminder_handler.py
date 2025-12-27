# [Task]: T091
# [Spec]: F-009 (R-009.1, R-009.2)
# [Description]: Reminder event handler for notification service
"""
Reminder event handler.
Processes reminder events and sends notifications to users.
"""
import logging
from typing import Dict, Any
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class ReminderHandler:
    """
    Handles reminder events from the task service.

    Processes reminder events received via Dapr pub/sub and
    sends appropriate notifications to users.
    """

    async def handle_reminder_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a reminder event from the task service.

        Args:
            event_data: The reminder event data from Dapr pub/sub

        Returns:
            Dict containing processing result
        """
        try:
            logger.info(f"Received reminder event: {event_data}")

            # Validate event data
            if not self._validate_event_data(event_data):
                return {
                    "status": "error",
                    "message": "Invalid reminder event data"
                }

            # Extract event details
            task_id = event_data.get("task_id")
            title = event_data.get("title")
            due_at = event_data.get("due_at")
            remind_at = event_data.get("remind_at")
            user_id = event_data.get("user_id")

            logger.info(f"Processing reminder for task '{title}' (ID: {task_id}) for user {user_id}")

            # Send notification
            notification_result = await self._send_notification(
                task_id=task_id,
                title=title,
                due_at=due_at,
                remind_at=remind_at,
                user_id=user_id
            )

            if notification_result["success"]:
                logger.info(f"Successfully sent reminder notification for task '{title}'")
                return {
                    "status": "success",
                    "message": f"Reminder notification sent for task '{title}'",
                    "task_id": task_id,
                    "user_id": user_id
                }
            else:
                logger.error(f"Failed to send reminder notification for task '{title}': {notification_result['message']}")
                return {
                    "status": "error",
                    "message": f"Failed to send notification: {notification_result['message']}",
                    "task_id": task_id,
                    "user_id": user_id
                }

        except Exception as e:
            logger.error(f"Unexpected error handling reminder event: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }

    def _validate_event_data(self, event_data: Dict[str, Any]) -> bool:
        """
        Validate the reminder event data.

        Args:
            event_data: The event data to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["task_id", "title", "user_id"]
        for field in required_fields:
            if field not in event_data or not event_data[field]:
                logger.warning(f"Missing required field: {field}")
                return False

        return True

    async def _send_notification(
        self,
        task_id: str,
        title: str,
        due_at: str = None,
        remind_at: str = None,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Send a notification to the user about the reminder.

        Args:
            task_id: The task ID
            title: The task title
            due_at: The due date (optional)
            remind_at: The reminder time (optional)
            user_id: The user ID

        Returns:
            Dict containing notification result
        """
        try:
            # For now, we'll log the notification
            # In a real implementation, this would integrate with email/SMS/push services

            notification_message = f"Reminder: Task '{title}' is due"

            if due_at:
                try:
                    due_datetime = datetime.fromisoformat(due_at.replace("Z", "+00:00"))
                    notification_message += f" on {due_datetime.strftime('%Y-%m-%d %H:%M')}"
                except ValueError:
                    notification_message += f" on {due_at}"

            if remind_at:
                try:
                    remind_datetime = datetime.fromisoformat(remind_at.replace("Z", "+00:00"))
                    notification_message += f" (reminder set for {remind_datetime.strftime('%Y-%m-%d %H:%M')})"
                except ValueError:
                    pass

            logger.info(f"Sending notification to user {user_id}: {notification_message}")

            # Simulate notification sending
            # In production, this would call external services like:
            # - Email service (SendGrid, AWS SES, etc.)
            # - SMS service (Twilio, AWS SNS, etc.)
            # - Push notification service (Firebase, etc.)

            # For this implementation, we'll just log it
            print(f"NOTIFICATION: {notification_message}")

            return {
                "success": True,
                "message": "Notification sent successfully",
                "notification_type": "console_log"
            }

        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return {
                "success": False,
                "message": f"Notification sending failed: {str(e)}"
            }


# Singleton instance
reminder_handler = ReminderHandler()
