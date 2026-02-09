"""Integration tests for offer tool."""

from unittest.mock import AsyncMock, patch

import pytest

from notch_chatbot.adapters.email_adapter import EmailServiceAdapter
from notch_chatbot.services.email_strategy import SendGridEmailService
from notch_chatbot.services.proposal_service import ProposalGenerator
from notch_chatbot.tools import create_offer_tool


@pytest.mark.asyncio
async def test_create_and_send_offer_integration():
    """Test complete offer creation flow."""
    mock_response = AsyncMock()
    mock_response.status_code = 202

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.return_value = (
            mock_response
        )

        email_service = SendGridEmailService("test_api_key")
        email_adapter = EmailServiceAdapter(email_service)
        proposal_generator = ProposalGenerator()

        offer_tool = create_offer_tool(email_adapter, proposal_generator)

        result = await offer_tool(
            client_name="John Smith",
            client_email="john@example.com",
            project_description="AI-powered inventory system",
            services_list="Custom Software Development, AI Engineering",
            project_scope="medium",
        )

        assert "success" in result.lower() or "sent" in result.lower()


@pytest.mark.asyncio
async def test_create_and_send_offer_small_scope():
    """Test offer creation with small scope."""
    mock_response = AsyncMock()
    mock_response.status_code = 202

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.return_value = (
            mock_response
        )

        email_service = SendGridEmailService("test_api_key")
        email_adapter = EmailServiceAdapter(email_service)
        proposal_generator = ProposalGenerator()

        offer_tool = create_offer_tool(email_adapter, proposal_generator)

        result = await offer_tool(
            client_name="Jane Doe",
            client_email="jane@example.com",
            project_description="Simple MVP mobile app",
            services_list="Custom Software Development",
            project_scope="small",
        )

        assert "success" in result.lower() or "sent" in result.lower()


@pytest.mark.asyncio
async def test_create_and_send_offer_large_scope():
    """Test offer creation with large scope."""
    mock_response = AsyncMock()
    mock_response.status_code = 202

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.return_value = (
            mock_response
        )

        email_service = SendGridEmailService("test_api_key")
        email_adapter = EmailServiceAdapter(email_service)
        proposal_generator = ProposalGenerator()

        offer_tool = create_offer_tool(email_adapter, proposal_generator)

        result = await offer_tool(
            client_name="Enterprise Corp",
            client_email="contact@enterprise.com",
            project_description="Complex enterprise platform with multiple systems integration",
            services_list="Custom Software Development, AI Engineering, Enterprise Integration",
            project_scope="large",
        )

        assert "success" in result.lower() or "sent" in result.lower()


@pytest.mark.asyncio
async def test_create_and_send_offer_error_handling():
    """Test error handling in offer creation."""
    mock_response = AsyncMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.return_value = (
            mock_response
        )

        email_service = SendGridEmailService("test_api_key")
        email_adapter = EmailServiceAdapter(email_service)
        proposal_generator = ProposalGenerator()

        offer_tool = create_offer_tool(email_adapter, proposal_generator)

        result = await offer_tool(
            client_name="Test User",
            client_email="test@example.com",
            project_description="Test project",
            services_list="Test Service",
            project_scope="medium",
        )

        assert "error" in result.lower()
