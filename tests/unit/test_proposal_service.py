"""Unit tests for proposal generator."""

from notch_chatbot.services.proposal_service import ProposalGenerator


def test_proposal_generator():
    """Test PDF generation."""
    generator = ProposalGenerator()

    pdf_content = generator.generate(
        client_name="Test Client",
        project_description="Test project description",
        services_list="Custom Software, AI Engineering",
        project_scope="medium",
    )

    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 0
    # PDF magic number check
    assert pdf_content.startswith(b"%PDF")


def test_proposal_generator_small_scope():
    """Test PDF generation with small scope."""
    generator = ProposalGenerator()

    pdf_content = generator.generate(
        client_name="Small Client",
        project_description="MVP mobile app",
        services_list="Custom Software Development",
        project_scope="small",
    )

    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 0
    assert pdf_content.startswith(b"%PDF")


def test_proposal_generator_large_scope():
    """Test PDF generation with large scope."""
    generator = ProposalGenerator()

    pdf_content = generator.generate(
        client_name="Enterprise Client",
        project_description="Complex enterprise platform with multiple integrations",
        services_list="Custom Software, AI Engineering, Enterprise Integration",
        project_scope="large",
    )

    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 0
    assert pdf_content.startswith(b"%PDF")


def test_proposal_generator_long_description():
    """Test PDF generation with long project description."""
    generator = ProposalGenerator()

    long_description = " ".join(["Test description"] * 50)  # Long text

    pdf_content = generator.generate(
        client_name="Test Client",
        project_description=long_description,
        services_list="Custom Software",
        project_scope="medium",
    )

    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 0
    assert pdf_content.startswith(b"%PDF")
