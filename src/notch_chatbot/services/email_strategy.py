"""Email sending via SendGrid."""

import base64
from dataclasses import dataclass

import httpx


@dataclass
class EmailMessage:
    """Value object for email content."""

    to_email: str
    to_name: str
    subject: str
    html_body: str
    attachments: list[tuple[str, bytes, str]]  # (filename, content, mime_type)


class SendGridEmailService:
    """SendGrid email service."""

    def __init__(self, api_key: str, sender_email: str = "proposals@wearenotch.com"):
        """Initialize SendGrid service.

        Args:
            api_key: SendGrid API key
            sender_email: Email address to send from
        """
        self.api_key = api_key
        self.sender_email = sender_email

    async def send(self, message: EmailMessage) -> tuple[bool, str]:
        """Send email via SendGrid API."""
        try:
            email_data = self._build_sendgrid_payload(message)

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.sendgrid.com/v3/mail/send",
                    json=email_data,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                )

                if response.status_code == 202:
                    return True, f"Proposal sent successfully to {message.to_email}"
                else:
                    return (
                        False,
                        f"SendGrid error: {response.status_code} - {response.text}",
                    )

        except Exception as e:
            return False, f"Email sending failed: {str(e)}"

    def _build_sendgrid_payload(self, message: EmailMessage) -> dict:
        """Build SendGrid API payload."""
        payload = {
            "personalizations": [
                {
                    "to": [{"email": message.to_email, "name": message.to_name}],
                    "subject": message.subject,
                }
            ],
            "from": {"email": self.sender_email, "name": "Notch Team"},
            "content": [{"type": "text/html", "value": message.html_body}],
        }

        if message.attachments:
            payload["attachments"] = [
                {
                    "content": base64.b64encode(content).decode(),
                    "filename": filename,
                    "type": mime_type,
                    "disposition": "attachment",
                }
                for filename, content, mime_type in message.attachments
            ]

        return payload
