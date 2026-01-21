"""Data models for Notch chatbot knowledge base."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ServiceCategory(str, Enum):
    """Service categories offered by Notch."""

    PLAN = "plan"
    DESIGN = "design"
    BUILD = "build"
    INTEGRATE = "integrate"


class Industry(str, Enum):
    """Industries served by Notch."""

    MANUFACTURING = "manufacturing"
    AUTOMOTIVE = "automotive"
    PHARMA = "pharma"
    TELCO = "telco"
    FINTECH = "fintech"
    HEALTHCARE = "healthcare"
    ENERGY = "energy"
    WORKFORCE_MANAGEMENT = "workforce_management"
    IOT = "iot"
    ENTERPRISE = "enterprise"
    RETAIL = "retail"
    LOGISTICS = "logistics"
    SAAS = "saas"


class ExpertiseDomain(str, Enum):
    """Technical expertise domains at Notch."""

    AI_ENGINEERING = "ai_engineering"
    SOFTWARE_ENGINEERING = "software_engineering"
    QUALITY_ENGINEERING = "quality_engineering"
    PRODUCT_MANAGEMENT = "product_management"
    IAM = "identity_access_management"
    CLOUD_DEVOPS = "cloud_devops"
    BPM = "bpm_solutions"
    IOT = "iot_solutions"


class Service(BaseModel):
    """A service offering from Notch."""

    id: str
    name: str
    category: ServiceCategory
    description: str
    short_description: str = Field(
        ..., description="1-2 sentence summary for chat"
    )
    key_features: list[str]
    related_expertise: list[ExpertiseDomain]
    typical_timeline: Optional[str] = None
    ideal_for: list[str] = Field(
        default_factory=list, description="Client scenarios"
    )
    url: str


class CaseStudy(BaseModel):
    """A customer success story."""

    id: str
    client_name: str
    title: str
    industry: Industry
    services_used: list[str] = Field(
        ..., description="Service IDs used in this project"
    )
    challenge: str
    solution: str
    outcome: Optional[str] = None
    technologies: list[str] = Field(default_factory=list)
    partnership_duration: Optional[str] = None
    quote: Optional[str] = None
    metrics: Optional[list[str]] = None
    url: str


class UseCase(BaseModel):
    """A use case demonstrating Notch's capabilities."""

    id: str
    title: str
    domain: ExpertiseDomain
    problem: str
    solution: str
    metric: Optional[str] = None
    related_services: list[str]
    url: str


class KnowledgeBase(BaseModel):
    """Complete knowledge base for the chatbot."""

    services: list[Service]
    case_studies: list[CaseStudy]
    use_cases: list[UseCase]
    expertise_domains: dict[str, str] = Field(
        ..., description="Domain key to description mapping"
    )
