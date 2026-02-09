"""Unit tests for email service."""

from unittest.mock import AsyncMock, patch

import pytest

from notch_chatbot.services.email_strategy import EmailMessage, SendGridEmailService


@pytest.mark.asyncio
async def test_sendgrid_email_service_success():
    """Test SendGrid email service sends successfully."""
    mock_response = AsyncMock()
    mock_response.status_code = 202
    mock_response.text = "Accepted"

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.return_value = (
            mock_response
        )

        service = SendGridEmailService("test_api_key")
        message = EmailMessage(
            to_email="test@example.com",
            to_name="Test User",
            subject="Test Subject",
            html_body="<p>Test body</p>",
            attachments=[("test.pdf", b"content", "application/pdf")],
        )

        success, msg = await service.send(message)

        assert success is True
        assert "sent successfully" in msg.lower()


@pytest.mark.asyncio
async def test_sendgrid_email_service_error():
    """Test SendGrid email service handles errors."""
    mock_response = AsyncMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.return_value = (
            mock_response
        )

        service = SendGridEmailService("invalid_key")
        message = EmailMessage(
            to_email="test@example.com",
            to_name="Test User",
            subject="Test Subject",
            html_body="<p>Test body</p>",
            attachments=[],
        )

        success, msg = await service.send(message)

        assert success is False
        assert "401" in msg


@pytest.mark.asyncio
async def test_email_adapter():
    """Test email adapter formats proposal correctly."""
    from notch_chatbot.adapters.email_adapter import EmailServiceAdapter

    mock_response = AsyncMock()
    mock_response.status_code = 202

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.return_value = (
            mock_response
        )

        service = SendGridEmailService("test_api_key")
        adapter = EmailServiceAdapter(service)

        success, msg = await adapter.send_proposal(
            client_name="John Smith",
            client_email="john@test.com",
            pdf_content=b"fake pdf content",
            project_summary="AI project",
        )

        assert success is True


@pytest.mark.asyncio
async def test_email_message_dataclass():
    """Test EmailMessage dataclass creation."""
    message = EmailMessage(
        to_email="test@example.com",
        to_name="Test User",
        subject="Test Subject",
        html_body="<p>Test</p>",
        attachments=[],
    )

    assert message.to_email == "test@example.com"
    assert message.to_name == "Test User"
    assert message.subject == "Test Subject"
    assert message.html_body == "<p>Test</p>"
    assert message.attachments == []
