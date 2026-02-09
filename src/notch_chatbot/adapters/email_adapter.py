"""Email service adapter for business logic."""

from datetime import datetime

from ..services.email_strategy import EmailMessage, SendGridEmailService


class EmailServiceAdapter:
    """Adapter to isolate email implementation details from business logic."""

    def __init__(self, email_service: SendGridEmailService):
        """Initialize adapter with email service.

        Args:
            email_service: SendGrid email service instance
        """
        self._email_service = email_service

    async def send_proposal(
        self,
        client_name: str,
        client_email: str,
        pdf_content: bytes,
        project_summary: str,
    ) -> tuple[bool, str]:
        """Send proposal email with PDF attachment.

        Args:
            client_name: Client's name
            client_email: Client's email address
            pdf_content: PDF file content as bytes
            project_summary: Brief project description for email body

        Returns:
            Tuple of (success: bool, message: str)
        """
        message = EmailMessage(
            to_email=client_email,
            to_name=client_name,
            subject=f"Your Project Proposal from Notch - {datetime.now().strftime('%B %Y')}",
            html_body=self._format_proposal_email(client_name, project_summary),
            attachments=[
                (
                    f"Notch_Proposal_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    pdf_content,
                    "application/pdf",
                )
            ],
        )

        return await self._email_service.send(message)

    def _format_proposal_email(self, client_name: str, summary: str) -> str:
        """Format proposal email HTML body."""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #0066cc;">Hello {client_name},</h2>

                <p>Thank you for your interest in working with Notch! We're excited about the opportunity to help bring your project to life.</p>

                <p>Attached to this email, you'll find a detailed proposal outlining:</p>
                <ul>
                    <li>Project overview and our understanding of your needs</li>
                    <li>Recommended services and approach</li>
                    <li>Team composition</li>
                    <li>Investment estimate</li>
                    <li>Next steps</li>
                </ul>

                <p>Please review the proposal at your convenience. We'd be happy to schedule a call to discuss any questions you might have and dive deeper into the details.</p>

                <p>Looking forward to hearing from you!</p>

                <p style="margin-top: 30px;">
                    <strong>Best regards,</strong><br>
                    The Notch Team<br>
                    <a href="https://www.wearenotch.com" style="color: #0066cc;">www.wearenotch.com</a>
                </p>
            </body>
        </html>
        """
