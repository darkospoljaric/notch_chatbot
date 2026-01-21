"""Tools for the Notch chatbot agent."""

import httpx
from pydantic_ai import RunContext

from .models import CaseStudy, Industry, KnowledgeBase, Service, UseCase


def find_services_by_keyword(
    ctx: RunContext[KnowledgeBase], keywords: list[str]
) -> list[Service]:
    """Find services matching given keywords.

    Searches across service names, descriptions, and key features.

    Args:
        ctx: Agent context containing knowledge base
        keywords: List of keywords to search for

    Returns:
        List of matching services
    """
    kb = ctx.deps
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
    ctx: RunContext[KnowledgeBase], category: str
) -> list[Service]:
    """Find all services in a specific category.

    Args:
        ctx: Agent context containing knowledge base
        category: Service category (plan, design, build, integrate)

    Returns:
        List of services in the category
    """
    kb = ctx.deps
    return [s for s in kb.services if s.category.value == category.lower()]


def find_case_studies_by_industry(
    ctx: RunContext[KnowledgeBase], industry: str
) -> list[CaseStudy]:
    """Find case studies for a specific industry.

    Args:
        ctx: Agent context containing knowledge base
        industry: Industry name

    Returns:
        List of case studies in that industry
    """
    kb = ctx.deps
    industry_lower = industry.lower().replace(" ", "_")

    matches = []
    for cs in kb.case_studies:
        if cs.industry.value == industry_lower:
            matches.append(cs)

    return matches


def find_case_studies_by_service(
    ctx: RunContext[KnowledgeBase], service_id: str
) -> list[CaseStudy]:
    """Find case studies that used a specific service.

    Args:
        ctx: Agent context containing knowledge base
        service_id: Service ID to search for

    Returns:
        List of case studies using that service
    """
    kb = ctx.deps
    return [cs for cs in kb.case_studies if service_id in cs.services_used]


def find_similar_case_studies(
    ctx: RunContext[KnowledgeBase], keywords: list[str]
) -> list[CaseStudy]:
    """Find case studies matching keywords in challenge, solution, or outcome.

    Args:
        ctx: Agent context containing knowledge base
        keywords: Keywords to search for

    Returns:
        List of matching case studies
    """
    kb = ctx.deps
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


def get_all_case_studies(ctx: RunContext[KnowledgeBase]) -> list[CaseStudy]:
    """Get all available case studies.

    Args:
        ctx: Agent context containing knowledge base

    Returns:
        List of all case studies
    """
    return ctx.deps.case_studies


def find_use_cases_by_domain(
    ctx: RunContext[KnowledgeBase], domain: str
) -> list[UseCase]:
    """Find use cases for a specific expertise domain.

    Args:
        ctx: Agent context containing knowledge base
        domain: Expertise domain

    Returns:
        List of use cases in that domain
    """
    kb = ctx.deps
    domain_lower = domain.lower().replace(" ", "_")

    return [uc for uc in kb.use_cases if uc.domain.value == domain_lower]


def get_expertise_description(
    ctx: RunContext[KnowledgeBase], domain: str
) -> str | None:
    """Get description for a specific expertise domain.

    Args:
        ctx: Agent context containing knowledge base
        domain: Expertise domain key

    Returns:
        Description of the expertise domain or None if not found
    """
    kb = ctx.deps
    return kb.expertise_domains.get(domain)


def list_all_services(ctx: RunContext[KnowledgeBase]) -> list[Service]:
    """List all available services.

    Args:
        ctx: Agent context containing knowledge base

    Returns:
        List of all services
    """
    return ctx.deps.services


def list_available_industries(ctx: RunContext[KnowledgeBase]) -> list[str]:
    """List all industries we have case studies for.

    Args:
        ctx: Agent context containing knowledge base

    Returns:
        List of industry names
    """
    return sorted({cs.industry.value for cs in ctx.deps.case_studies})


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
            content = response.text

            # Return a note that this is available
            return (
                "Blog posts are available at https://www.wearenotch.com/resources/blog. "
                "The blog covers topics in AI, software development, best practices, and case studies."
            )
    except Exception as e:
        return f"Unable to fetch blog posts at this time. Visit https://www.wearenotch.com/resources/blog for latest content. Error: {str(e)}"
