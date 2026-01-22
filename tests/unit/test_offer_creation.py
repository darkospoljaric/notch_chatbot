"""Unit tests for PDF offer creation."""

import base64
import os
from unittest.mock import AsyncMock, patch

import pytest

from notch_chatbot.tools import create_and_send_offer


class TestPDFOfferCreation:
    """Test PDF offer generation functionality."""

    @pytest.mark.asyncio
    async def test_offer_creation_requires_sendgrid_key(self):
        """Test that offer creation fails gracefully without SendGrid key."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove SENDGRID_API_KEY from environment
            result = await create_and_send_offer(
                client_name="John Doe",
                client_email="john@example.com",
                project_description="A test project for inventory management",
                services_list="Custom Software Development, AI Engineering",
                project_scope="medium",
            )

            assert "Error: SENDGRID_API_KEY not configured" in result
            assert "sendgrid.com" in result.lower()

    @pytest.mark.asyncio
    async def test_offer_creation_with_small_scope(self):
        """Test PDF generation with small project scope."""
        # Mock SendGrid API response
        mock_response = AsyncMock()
        mock_response.status_code = 202
        mock_response.text = "Accepted"

        with patch.dict(os.environ, {"SENDGRID_API_KEY": "test_key_123"}, clear=False):
            with patch("httpx.AsyncClient") as mock_client:
                mock_client.return_value.__aenter__.return_value.post.return_value = (
                    mock_response
                )

                result = await create_and_send_offer(
                    client_name="Jane Smith",
                    client_email="jane@example.com",
                    project_description="Simple mobile app for task management",
                    services_list="Mobile App Development, UI/UX Design",
                    project_scope="small",
                )

                assert "✓ Offer sent successfully" in result
                assert "jane@example.com" in result

    @pytest.mark.asyncio
    async def test_offer_creation_with_medium_scope(self):
        """Test PDF generation with medium project scope (default)."""
        mock_response = AsyncMock()
        mock_response.status_code = 202

        with patch.dict(os.environ, {"SENDGRID_API_KEY": "test_key_456"}, clear=False):
            with patch("httpx.AsyncClient") as mock_client:
                mock_client.return_value.__aenter__.return_value.post.return_value = (
                    mock_response
                )

                result = await create_and_send_offer(
                    client_name="Bob Wilson",
                    client_email="bob@company.com",
                    project_description="B2B platform for supply chain management with real-time tracking",
                    services_list="Custom Software Development, Enterprise Integration",
                    project_scope="medium",
                )

                assert "✓ Offer sent successfully" in result
                assert "bob@company.com" in result

    @pytest.mark.asyncio
    async def test_offer_creation_with_large_scope(self):
        """Test PDF generation with large project scope."""
        mock_response = AsyncMock()
        mock_response.status_code = 202

        with patch.dict(os.environ, {"SENDGRID_API_KEY": "test_key_789"}, clear=False):
            with patch("httpx.AsyncClient") as mock_client:
                mock_client.return_value.__aenter__.return_value.post.return_value = (
                    mock_response
                )

                result = await create_and_send_offer(
                    client_name="Alice Johnson",
                    client_email="alice@enterprise.com",
                    project_description="Enterprise-wide platform with AI, microservices, and global deployment",
                    services_list="Custom Software Development, AI Engineering, Cloud Architecture, DevOps",
                    project_scope="large",
                )

                assert "✓ Offer sent successfully" in result
                assert "alice@enterprise.com" in result

    @pytest.mark.asyncio
    async def test_offer_no_bcc_recipients(self):
        """Test that BCC recipients are NOT included in email."""
        mock_response = AsyncMock()
        mock_response.status_code = 202

        with patch.dict(os.environ, {"SENDGRID_API_KEY": "test_key_bcc"}, clear=False):
            with patch("httpx.AsyncClient") as mock_client:
                mock_post = AsyncMock(return_value=mock_response)
                mock_client.return_value.__aenter__.return_value.post = mock_post

                await create_and_send_offer(
                    client_name="Test User",
                    client_email="test@example.com",
                    project_description="Test project",
                    services_list="Testing",
                    project_scope="medium",
                )

                # Verify post was called
                assert mock_post.called

                # Get the call arguments
                call_args = mock_post.call_args

                # Check JSON data does NOT include BCC
                json_data = call_args.kwargs["json"]
                assert "bcc" not in json_data

    @pytest.mark.asyncio
    async def test_offer_pdf_attachment_structure(self):
        """Test that PDF is properly attached to email."""
        mock_response = AsyncMock()
        mock_response.status_code = 202

        with patch.dict(os.environ, {"SENDGRID_API_KEY": "test_key_pdf"}, clear=False):
            with patch("httpx.AsyncClient") as mock_client:
                mock_post = AsyncMock(return_value=mock_response)
                mock_client.return_value.__aenter__.return_value.post = mock_post

                await create_and_send_offer(
                    client_name="PDF Test",
                    client_email="pdf@example.com",
                    project_description="Testing PDF attachment",
                    services_list="Testing Services",
                    project_scope="medium",
                )

                # Get the call arguments
                call_args = mock_post.call_args
                json_data = call_args.kwargs["json"]

                # Check attachment
                attachments = json_data["attachments"]
                assert len(attachments) == 1

                attachment = attachments[0]
                assert attachment["type"] == "application/pdf"
                assert attachment["disposition"] == "attachment"
                assert "Notch_Proposal_PDF_Test" in attachment["filename"]
                assert attachment["filename"].endswith(".pdf")

                # Verify content is base64 encoded
                content = attachment["content"]
                assert isinstance(content, str)
                assert len(content) > 0

                # Try to decode to verify it's valid base64
                try:
                    base64.b64decode(content)
                except Exception as e:
                    pytest.fail(f"PDF content is not valid base64: {e}")

    @pytest.mark.asyncio
    async def test_offer_email_subject_format(self):
        """Test that email subject is properly formatted."""
        mock_response = AsyncMock()
        mock_response.status_code = 202

        with patch.dict(
            os.environ, {"SENDGRID_API_KEY": "test_key_subject"}, clear=False
        ):
            with patch("httpx.AsyncClient") as mock_client:
                mock_post = AsyncMock(return_value=mock_response)
                mock_client.return_value.__aenter__.return_value.post = mock_post

                await create_and_send_offer(
                    client_name="Subject Test",
                    client_email="subject@example.com",
                    project_description="Testing email subject",
                    services_list="Testing",
                    project_scope="small",
                )

                call_args = mock_post.call_args
                json_data = call_args.kwargs["json"]

                subject = json_data["personalizations"][0]["subject"]
                assert "Your Project Proposal from Notch" in subject
                # Subject should include month and year

    @pytest.mark.asyncio
    async def test_offer_sendgrid_error_handling(self):
        """Test handling of SendGrid API errors."""
        mock_response = AsyncMock()
        mock_response.status_code = 401
        mock_response.text = '{"errors":[{"message":"Invalid API key"}]}'

        with patch.dict(os.environ, {"SENDGRID_API_KEY": "invalid_key"}, clear=False):
            with patch("httpx.AsyncClient") as mock_client:
                mock_client.return_value.__aenter__.return_value.post.return_value = (
                    mock_response
                )

                result = await create_and_send_offer(
                    client_name="Error Test",
                    client_email="error@example.com",
                    project_description="Testing error handling",
                    services_list="Testing",
                    project_scope="medium",
                )

                assert "Error sending email" in result
                assert "401" in result

    @pytest.mark.asyncio
    async def test_offer_network_exception_handling(self):
        """Test handling of network exceptions."""
        with patch.dict(
            os.environ, {"SENDGRID_API_KEY": "test_key_network"}, clear=False
        ):
            with patch("httpx.AsyncClient") as mock_client:
                # Simulate network error
                mock_client.return_value.__aenter__.return_value.post.side_effect = (
                    Exception("Network error")
                )

                result = await create_and_send_offer(
                    client_name="Network Test",
                    client_email="network@example.com",
                    project_description="Testing network errors",
                    services_list="Testing",
                    project_scope="large",
                )

                assert "Error sending offer email" in result
                assert "Network error" in result

    @pytest.mark.asyncio
    async def test_offer_sender_email_is_hardcoded(self):
        """Test that sender email is proposals@wearenotch.com."""
        mock_response = AsyncMock()
        mock_response.status_code = 202

        with patch.dict(
            os.environ, {"SENDGRID_API_KEY": "test_key_sender"}, clear=False
        ):
            with patch("httpx.AsyncClient") as mock_client:
                mock_post = AsyncMock(return_value=mock_response)
                mock_client.return_value.__aenter__.return_value.post = mock_post

                await create_and_send_offer(
                    client_name="Sender Test",
                    client_email="sender@example.com",
                    project_description="Testing sender email",
                    services_list="Testing",
                    project_scope="medium",
                )

                call_args = mock_post.call_args
                json_data = call_args.kwargs["json"]

                from_email = json_data["from"]["email"]
                from_name = json_data["from"]["name"]

                assert from_email == "proposals@wearenotch.com"
                assert from_name == "Notch Team"

    @pytest.mark.asyncio
    async def test_offer_default_scope_is_medium(self):
        """Test that default project scope is medium."""
        mock_response = AsyncMock()
        mock_response.status_code = 202

        with patch.dict(
            os.environ, {"SENDGRID_API_KEY": "test_key_default"}, clear=False
        ):
            with patch("httpx.AsyncClient") as mock_client:
                mock_post = AsyncMock(return_value=mock_response)
                mock_client.return_value.__aenter__.return_value.post = mock_post

                # Don't specify project_scope, should default to medium
                result = await create_and_send_offer(
                    client_name="Default Test",
                    client_email="default@example.com",
                    project_description="Testing default scope",
                    services_list="Testing",
                )

                assert "✓ Offer sent successfully" in result


class TestPDFContentValidation:
    """Test that PDF contains expected content."""

    @pytest.mark.asyncio
    async def test_offer_includes_client_info(self):
        """Test that offer includes client name and email in PDF."""
        mock_response = AsyncMock()
        mock_response.status_code = 202

        client_name = "John Q. Public"
        client_email = "john.public@company.com"

        with patch.dict(
            os.environ, {"SENDGRID_API_KEY": "test_key_content"}, clear=False
        ):
            with patch("httpx.AsyncClient") as mock_client:
                mock_post = AsyncMock(return_value=mock_response)
                mock_client.return_value.__aenter__.return_value.post = mock_post

                await create_and_send_offer(
                    client_name=client_name,
                    client_email=client_email,
                    project_description="Test project for content validation",
                    services_list="Software Development",
                    project_scope="medium",
                )

                call_args = mock_post.call_args
                json_data = call_args.kwargs["json"]

                # Check that client info is in email recipient
                to_email = json_data["personalizations"][0]["to"][0]["email"]
                to_name = json_data["personalizations"][0]["to"][0]["name"]

                assert to_email == client_email
                assert to_name == client_name

    @pytest.mark.asyncio
    async def test_offer_filename_format(self):
        """Test that PDF filename is properly formatted."""
        mock_response = AsyncMock()
        mock_response.status_code = 202

        with patch.dict(
            os.environ, {"SENDGRID_API_KEY": "test_key_filename"}, clear=False
        ):
            with patch("httpx.AsyncClient") as mock_client:
                mock_post = AsyncMock(return_value=mock_response)
                mock_client.return_value.__aenter__.return_value.post = mock_post

                await create_and_send_offer(
                    client_name="Mary Jane Watson",
                    client_email="mary@example.com",
                    project_description="Testing filename format",
                    services_list="Testing",
                    project_scope="small",
                )

                call_args = mock_post.call_args
                json_data = call_args.kwargs["json"]

                filename = json_data["attachments"][0]["filename"]

                # Should be: Notch_Proposal_Mary_Jane_Watson_YYYYMMDD.pdf
                assert filename.startswith("Notch_Proposal_")
                assert "Mary_Jane_Watson" in filename
                assert filename.endswith(".pdf")
                # Should include date in YYYYMMDD format
                import re

                assert re.search(r"\d{8}\.pdf$", filename)
