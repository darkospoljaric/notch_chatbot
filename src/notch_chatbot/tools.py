"""Tools for the Notch chatbot agent."""

import logging
from typing import Annotated

import httpx
from pydantic_ai import RunContext

from .adapters.email_adapter import EmailServiceAdapter
from .models import AgentDeps, CaseStudy, Service, UseCase
from .services.proposal_service import ProposalGenerator

# Configure logging
logger = logging.getLogger(__name__)


def find_services_by_keyword(
    ctx: RunContext[AgentDeps], keywords: list[str]
) -> list[Service]:
    """Find services matching given keywords.

    Searches across service names, descriptions, and key features.

    Args:
        ctx: Agent context containing knowledge base
        keywords: List of keywords to search for

    Returns:
        List of matching services
    """
    kb = ctx.deps.kb
    matches = []
    keywords_lower = [k.lower() for k in keywords]

    for service in kb.services:
        # Create searchable text
        searchable = " ".join(
            [
                service.name,
                service.description,
                service.short_description,
                *service.key_features,
                *service.ideal_for,
            ]
        ).lower()

        # Check if any keyword matches
        if any(kw in searchable for kw in keywords_lower):
            matches.append(service)

    return matches


def find_services_by_category(
    ctx: RunContext[AgentDeps], category: str
) -> list[Service]:
    """Find all services in a specific category.

    Args:
        ctx: Agent context containing knowledge base
        category: Service category (plan, design, build, integrate)

    Returns:
        List of services in the category
    """
    kb = ctx.deps.kb
    return [s for s in kb.services if s.category.value == category.lower()]


def find_case_studies_by_industry(
    ctx: RunContext[AgentDeps], industry: str
) -> list[CaseStudy]:
    """Find case studies for a specific industry.

    Args:
        ctx: Agent context containing knowledge base
        industry: Industry name

    Returns:
        List of case studies in that industry
    """
    kb = ctx.deps.kb
    industry_lower = industry.lower().replace(" ", "_")

    matches = []
    for cs in kb.case_studies:
        if cs.industry.value == industry_lower:
            matches.append(cs)

    return matches


def find_case_studies_by_service(
    ctx: RunContext[AgentDeps], service_id: str
) -> list[CaseStudy]:
    """Find case studies that used a specific service.

    Args:
        ctx: Agent context containing knowledge base
        service_id: Service ID to search for

    Returns:
        List of case studies using that service
    """
    kb = ctx.deps.kb
    return [cs for cs in kb.case_studies if service_id in cs.services_used]


def find_similar_case_studies(
    ctx: RunContext[AgentDeps], keywords: list[str]
) -> list[CaseStudy]:
    """Find case studies matching keywords in challenge, solution, or outcome.

    Args:
        ctx: Agent context containing knowledge base
        keywords: Keywords to search for

    Returns:
        List of matching case studies
    """
    kb = ctx.deps.kb
    matches = []
    keywords_lower = [k.lower() for k in keywords]

    for cs in kb.case_studies:
        # Create searchable text
        searchable = " ".join(
            [
                cs.title,
                cs.challenge,
                cs.solution,
                cs.outcome or "",
                *cs.technologies,
            ]
        ).lower()

        # Check if any keyword matches
        if any(kw in searchable for kw in keywords_lower):
            matches.append(cs)

    return matches


def get_all_case_studies(ctx: RunContext[AgentDeps]) -> list[CaseStudy]:
    """Get all available case studies.

    Args:
        ctx: Agent context containing knowledge base

    Returns:
        List of all case studies
    """
    return ctx.deps.kb.case_studies


def find_use_cases_by_domain(ctx: RunContext[AgentDeps], domain: str) -> list[UseCase]:
    """Find use cases for a specific expertise domain.

    Args:
        ctx: Agent context containing knowledge base
        domain: Expertise domain

    Returns:
        List of use cases in that domain
    """
    kb = ctx.deps.kb
    domain_lower = domain.lower().replace(" ", "_")

    return [uc for uc in kb.use_cases if uc.domain.value == domain_lower]


def get_expertise_description(ctx: RunContext[AgentDeps], domain: str) -> str | None:
    """Get description for a specific expertise domain.

    Args:
        ctx: Agent context containing knowledge base
        domain: Expertise domain key

    Returns:
        Description of the expertise domain or None if not found
    """
    kb = ctx.deps.kb
    return kb.expertise_domains.get(domain)


def list_all_services(ctx: RunContext[AgentDeps]) -> list[Service]:
    """List all available services.

    Args:
        ctx: Agent context containing knowledge base

    Returns:
        List of all services
    """
    return ctx.deps.kb.services


def list_available_industries(ctx: RunContext[AgentDeps]) -> list[str]:
    """List all industries we have case studies for.

    Args:
        ctx: Agent context containing knowledge base

    Returns:
        List of industry names
    """
    return sorted({cs.industry.value for cs in ctx.deps.kb.case_studies})


async def fetch_latest_blog_posts(
    query: str = "latest posts", max_results: int = 3
) -> str:
    """Fetch latest blog posts from Notch website.

    Args:
        query: Search query for blog posts
        max_results: Maximum number of results to return

    Returns:
        Formatted string with blog post information
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.wearenotch.com/resources/blog",
                timeout=10.0,
                follow_redirects=True,
            )
            response.raise_for_status()

            # Simple extraction - in production you'd want proper HTML parsing
            # response.text contains the HTML content

            # Return a note that this is available
            return (
                "Blog posts are available at https://www.wearenotch.com/resources/blog. "
                "The blog covers topics in AI, software development, best practices, and case studies."
            )
    except Exception as e:
        return f"Unable to fetch blog posts at this time. Visit https://www.wearenotch.com/resources/blog for latest content. Error: {str(e)}"


def create_offer_tool(
    email_adapter: EmailServiceAdapter,
    proposal_generator: ProposalGenerator,
):
    """Factory function creating offer tool with injected dependencies.

    Args:
        email_adapter: Email service adapter
        proposal_generator: Proposal PDF generator

    Returns:
        Configured create_and_send_offer tool function
    """

    async def create_and_send_offer(
        client_name: Annotated[str, "Client's full name"],
        client_email: Annotated[str, "Client's email address"],
        project_description: Annotated[
            str, "Brief description of the project (2-4 sentences)"
        ],
        services_list: Annotated[
            str,
            "Comma-separated list of relevant Notch services (e.g., 'Custom Software Development, AI Engineering')",
        ],
        project_scope: Annotated[
            str,
            "Project scope: 'small' (simple apps, MVPs), 'medium' (standard B2B platforms), or 'large' (enterprise systems)",
        ] = "medium",
    ) -> str:
        """Create a proposal PDF and email it to the prospective client.

        This tool automatically generates a professional proposal document with pricing
        estimates and emails it to the client. Use when the client has expressed interest
        in receiving a detailed proposal.
        """
        logger.info(
            f"Starting offer creation for {client_name} ({client_email}), scope: {project_scope}"
        )

        try:
            # Generate PDF
            pdf_content = proposal_generator.generate(
                client_name=client_name,
                project_description=project_description,
                services_list=services_list,
                project_scope=project_scope,
            )

            # Send email
            success, message = await email_adapter.send_proposal(
                client_name=client_name,
                client_email=client_email,
                pdf_content=pdf_content,
                project_summary=project_description,
            )

            if success:
                logger.info(f"✓ Offer sent successfully to {client_email}")
                return f"✓ Offer sent successfully to {client_email}! {client_name} should receive it shortly."
            else:
                logger.error(f"Failed to send offer: {message}")
                return f"Error sending offer: {message}"

        except Exception as e:
            logger.exception(f"Exception while creating/sending offer: {e}")
            return f"Error creating or sending offer: {str(e)}"

    return create_and_send_offer
