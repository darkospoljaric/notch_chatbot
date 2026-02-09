"""Proposal generation service."""

from datetime import datetime

from fpdf import FPDF


class ProposalGenerator:
    """Service for generating proposal PDFs."""

    def generate(
        self,
        client_name: str,
        project_description: str,
        services_list: str,
        project_scope: str = "medium",
    ) -> bytes:
        """Generate proposal PDF.

        Args:
            client_name: Client's name
            project_description: Project description
            services_list: Comma-separated list of services
            project_scope: small, medium, or large

        Returns:
            PDF content as bytes
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Add content sections
        self._add_header(pdf)
        self._add_date(pdf)
        self._add_client_info(pdf, client_name)
        self._add_project_overview(pdf, project_description)
        self._add_services(pdf, services_list)
        self._add_team_composition(pdf)
        self._add_pricing(pdf, project_scope)
        self._add_next_steps(pdf)
        self._add_disclaimer(pdf)
        self._add_footer(pdf)

        # Get PDF as bytes (FPDF returns bytearray, convert to bytes)
        pdf_bytes = pdf.output(dest="S")
        return bytes(pdf_bytes)

    def _add_header(self, pdf: FPDF) -> None:
        """Add header with Notch branding."""
        pdf.set_font("Arial", "B", 24)
        pdf.set_text_color(0, 102, 204)  # Blue color for branding
        pdf.cell(0, 10, "NOTCH", ln=True, align="C")
        pdf.set_font("Arial", "I", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, "Software Development & AI Solutions", ln=True, align="C")
        pdf.ln(10)

    def _add_date(self, pdf: FPDF) -> None:
        """Add date to PDF."""
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 5, f"Date: {datetime.now().strftime('%B %d, %Y')}", ln=True)
        pdf.ln(5)

    def _add_client_info(self, pdf: FPDF, client_name: str) -> None:
        """Add client information section."""
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 7, "Proposal For:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, f"{client_name}", ln=True)
        pdf.ln(10)

    def _add_project_overview(self, pdf: FPDF, project_description: str) -> None:
        """Add project overview section."""
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 8, "Project Overview", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, project_description)
        pdf.ln(5)

    def _add_services(self, pdf: FPDF, services_list: str) -> None:
        """Add recommended services section."""
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 8, "Recommended Services", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, services_list)
        pdf.ln(5)

    def _add_team_composition(self, pdf: FPDF) -> None:
        """Add team composition section."""
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

    def _add_pricing(self, pdf: FPDF, project_scope: str) -> None:
        """Add pricing estimate section."""
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

    def _add_next_steps(self, pdf: FPDF) -> None:
        """Add next steps section."""
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

    def _add_disclaimer(self, pdf: FPDF) -> None:
        """Add disclaimer section."""
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

    def _add_footer(self, pdf: FPDF) -> None:
        """Add footer section."""
        pdf.set_y(-30)
        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, "Notch Software Development", ln=True, align="C")
        pdf.cell(0, 5, "www.wearenotch.com", ln=True, align="C")
