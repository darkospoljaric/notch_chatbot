"""Tools for the Notch chatbot agent."""

import base64
import os
from datetime import datetime
from io import BytesIO

import httpx
from fpdf import FPDF
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


async def create_and_send_offer(
    client_name: str,
    client_email: str,
    project_description: str,
    services_list: str,
    project_scope: str = "medium",
) -> str:
    """Create a PDF offer/proposal and send it via email to the prospect.

    Args:
        client_name: Name of the client/prospect
        client_email: Email address of the client
        project_description: Description of the project based on conversation
        services_list: Comma-separated list of relevant Notch services
        project_scope: Project size - "small", "medium", or "large" (affects pricing)

    Returns:
        Success or error message
    """
    try:
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Header with Notch branding
        pdf.set_font("Arial", "B", 24)
        pdf.set_text_color(0, 102, 204)  # Blue color for branding
        pdf.cell(0, 10, "NOTCH", ln=True, align="C")
        pdf.set_font("Arial", "I", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, "Software Development & AI Solutions", ln=True, align="C")
        pdf.ln(10)

        # Date
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 5, f"Date: {datetime.now().strftime('%B %d, %Y')}", ln=True)
        pdf.ln(5)

        # Client information
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 7, "Proposal For:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, f"{client_name}", ln=True)
        pdf.cell(0, 6, f"{client_email}", ln=True)
        pdf.ln(10)

        # Project overview
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 8, "Project Overview", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, project_description)
        pdf.ln(5)

        # Recommended services
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 8, "Recommended Services", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, services_list)
        pdf.ln(5)

        # Team composition
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 8, "Team Composition", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(
            0,
            6,
            "Your project will be handled by a dedicated team including:\n"
            "- Project Manager\n"
            "- Senior Software Engineers\n"
            "- UI/UX Designer\n"
            "- QA Specialist\n"
            "- DevOps Engineer (as needed)",
        )
        pdf.ln(5)

        # Pricing estimate
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 8, "Investment Estimate", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)

        # Determine pricing based on scope
        pricing_info = {
            "small": "Starting from $15,000 - $35,000",
            "medium": "Typical range: $35,000 - $100,000 depending on scope",
            "large": "Starting from $100,000+ depending on requirements",
        }

        pricing_text = pricing_info.get(project_scope.lower(), pricing_info["medium"])
        pdf.multi_cell(
            0,
            6,
            f"{pricing_text}\n\n"
            "Final pricing will be determined based on detailed requirements, "
            "timeline, and project complexity. We'll provide a detailed breakdown "
            "after our initial consultation call.",
        )
        pdf.ln(5)

        # Next steps
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 8, "Next Steps", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(
            0,
            6,
            "1. Review this proposal\n"
            "2. Schedule a consultation call to discuss details\n"
            "3. Receive detailed project plan and final quote\n"
            "4. Project kickoff and development",
        )
        pdf.ln(10)

        # Disclaimer
        pdf.set_font("Arial", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(
            0,
            5,
            "IMPORTANT: This proposal is for orientational purposes only and does not "
            "constitute a binding offer. Final terms, pricing, and deliverables will be "
            "confirmed in a formal contract following detailed requirements analysis.",
        )
        pdf.ln(5)

        # Footer
        pdf.set_y(-30)
        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, "Notch Software Development", ln=True, align="C")
        pdf.cell(0, 5, "www.wearenotch.com", ln=True, align="C")

        # Get PDF as bytes
        pdf_bytes = pdf.output(dest="S").encode("latin-1")
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

        # Now send the email with the PDF attached
        sendgrid_api_key = os.getenv("SENDGRID_API_KEY")

        if not sendgrid_api_key:
            return (
                "Error: SENDGRID_API_KEY not configured. Please set up SendGrid API key "
                "in environment variables. Get one at https://sendgrid.com (free tier: 100 emails/day)"
            )

        # SendGrid API endpoint
        url = "https://api.sendgrid.com/v3/mail/send"

        # Email content
        email_data = {
            "personalizations": [
                {
                    "to": [{"email": client_email, "name": client_name}],
                    "bcc": [
                        {"email": "darko.spoljaric@wearenotch.com"},
                        {"email": "sanja.buterin@wearenotch.com"},
                    ],
                    "subject": f"Your Project Proposal from Notch - {datetime.now().strftime('%B %Y')}",
                }
            ],
            "from": {
                "email": os.getenv(
                    "SENDGRID_FROM_EMAIL", "proposals@wearenotch.com"
                ),
                "name": "Notch Team",
            },
            "content": [
                {
                    "type": "text/html",
                    "value": f"""
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
                    """,
                }
            ],
            "attachments": [
                {
                    "content": pdf_base64,
                    "filename": f"Notch_Proposal_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    "type": "application/pdf",
                    "disposition": "attachment",
                }
            ],
        }

        # Send email via SendGrid
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=email_data,
                headers={
                    "Authorization": f"Bearer {sendgrid_api_key}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )

            if response.status_code == 202:
                return f"✓ Offer sent successfully to {client_email}! {client_name} should receive it shortly."
            else:
                return f"Error sending email: Status {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error sending offer email: {str(e)}"
